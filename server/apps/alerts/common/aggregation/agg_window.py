# -- coding: utf-8 --
# @File: agg_window.py
# @Time: 2025/7/4 14:37
# @Author: windyzhao

"""
聚合窗口处理器模块
包含滑动窗口、固定窗口、会话窗口的独立处理器
"""
import uuid
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
from collections import defaultdict

from django.db import transaction
from django.utils import timezone

from apps.alerts.common.aggregation.window_types import WindowCalculator
from apps.alerts.constants import AlertStatus
from apps.alerts.models import CorrelationRules, SessionWindow, Event, SessionEventRelation, Alert
from apps.alerts.common.aggregation.alert_processor import AlertProcessor
from apps.alerts.utils.util import generate_instance_fingerprint
from apps.core.logger import alert_logger as logger


class BaseWindowProcessor(ABC):
    """窗口处理器基类"""

    def __init__(self, window_size: str = "10min"):
        self.window_size = window_size
        self.processor = AlertProcessor(window_size=window_size)
        self.now = timezone.now()

    @property
    def fields(self):
        data = [
            "event_id", "external_id", "item", "received_at", "status", "level", "source__name",
            "source_id", "title", "rule_id", "description", "resource_id", "resource_type", "resource_name", "value"
        ]
        return data

    @abstractmethod
    def process_rules(self, rules: List[CorrelationRules]) -> Tuple[int, int]:
        """
        处理规则的抽象方法
        
        Args:
            rules: 要处理的规则列表
            
        Returns:
            Tuple[int, int]: (新建告警数, 更新告警数)
        """
        pass

    @abstractmethod
    def get_window_type(self) -> str:
        """获取窗口类型"""
        pass

    def _group_rules_by_window_size(self, rules: List[CorrelationRules]) -> Dict[str, List[CorrelationRules]]:
        """
        按窗口大小分组规则
        
        Args:
            rules: 规则列表
            
        Returns:
            Dict[str, List[CorrelationRules]]: 按窗口大小分组的规则
        """
        grouped_rules = defaultdict(list)
        for rule in rules:
            # 根据窗口类型获取相应的窗口大小
            if self.get_window_type() == 'session':
                window_size = getattr(rule, 'session_timeout', '10min')
            else:
                window_size = getattr(rule, 'window_size', '10min')
            grouped_rules[window_size].append(rule)
        return dict(grouped_rules)

    def _execute_processing(self, format_alert_list: List[Dict[str, Any]],
                            update_alert_list: List[Dict[str, Any]]) -> Tuple[int, int]:
        """执行告警创建和更新的公共方法"""
        alerts_created = 0
        alerts_updated = len(update_alert_list)

        try:
            if format_alert_list:
                created_ids = self.processor.bulk_create_alerts(alerts=format_alert_list)
                alerts_created = len(created_ids)
                if created_ids:
                    self.processor.alert_auto_assign(alert_id_list=created_ids)

            if update_alert_list:
                self.processor.update_alerts(alerts=update_alert_list)

        except Exception as e:
            logger.error(f"执行{self.get_window_type()}窗口告警处理失败: {str(e)}")

        return alerts_created, alerts_updated


class SlidingWindowProcessor(BaseWindowProcessor):
    """滑动窗口处理器
    
    特点：
    - 每分钟都执行
    - 窗口持续滑动
    - 适用于实时监控场景
    """

    def get_window_type(self) -> str:
        return "sliding"

    def process_rules(self, rules: List[CorrelationRules]) -> Tuple[int, int]:
        """
        处理滑动窗口规则
        
        滑动窗口处理逻辑：
        1. 按窗口大小分组处理
        2. 每个窗口大小使用专门的处理器
        3. 实时性要求高，每分钟执行一次
        """
        logger.info(f"开始处理滑动窗口规则，数量: {len(rules)}")

        # 按窗口大小分组规则
        grouped_rules = self._group_rules_by_window_size(rules)

        total_format_alerts = []
        total_update_alerts = []

        # 按窗口大小分组处理
        for window_size, size_rules in grouped_rules.items():
            logger.info(f"处理窗口大小 {window_size} 的滑动窗口规则，数量: {len(size_rules)}")

            try:
                # 为每个窗口大小创建专门的处理器
                processor = AlertProcessor(window_size=window_size)

                # 性能优化：只加载当前需要的规则
                processor.set_target_correlation_rules(size_rules)
                processor.reload_database_rules()

                # 批量处理该窗口大小的规则
                batch_alerts, batch_updates = processor._process_batch_correlation_rules(
                    size_rules, self.get_window_type()
                )

                total_format_alerts.extend(batch_alerts)
                total_update_alerts.extend(batch_updates)

                logger.info(
                    f"窗口大小 {window_size} 处理完成，产生 {len(batch_alerts)} 个新告警，{len(batch_updates)} 个更新")

            except Exception as e:
                logger.error(f"窗口大小 {window_size} 的滑动窗口规则处理失败: {str(e)}")
                continue

        logger.info(f"滑动窗口处理完成，总计产生 {len(total_format_alerts)} 个新告警，{len(total_update_alerts)} 个更新")

        return self._execute_processing(total_format_alerts, total_update_alerts)


class FixedWindowProcessor(BaseWindowProcessor):
    """固定窗口处理器
    
    特点：
    - 按时间对齐执行（如每5分钟、每小时）
    - 窗口边界固定
    - 适用于定期统计场景
    """

    def get_window_type(self) -> str:
        return "fixed"

    def process_rules(self, rules: List[CorrelationRules]) -> Tuple[int, int]:
        """
        处理固定窗口规则
        
        固定窗口处理逻辑：
        1. 按窗口大小分组处理
        2. 每个窗口大小使用专门的处理器
        3. 按窗口对齐方式确定执行时间
        """
        logger.info(f"开始处理固定窗口规则，数量: {len(rules)}")

        # 按窗口大小分组规则
        grouped_rules = self._group_rules_by_window_size(rules)

        total_format_alerts = []
        total_update_alerts = []

        # 按窗口大小分组处理
        for window_size, size_rules in grouped_rules.items():
            logger.info(f"处理窗口大小 {window_size} 的固定窗口规则，数量: {len(size_rules)}")

            try:
                # 为每个窗口大小创建专门的处理器
                processor = AlertProcessor(window_size=window_size)

                # 性能优化：只加载当前需要的规则
                processor.set_target_correlation_rules(size_rules)
                processor.reload_database_rules()

                # 批量处理该窗口大小的规则
                batch_alerts, batch_updates = processor._process_batch_correlation_rules(
                    size_rules, self.get_window_type()
                )

                total_format_alerts.extend(batch_alerts)
                total_update_alerts.extend(batch_updates)

                logger.info(
                    f"窗口大小 {window_size} 处理完成，产生 {len(batch_alerts)} 个新告警，{len(batch_updates)} 个更新")

            except Exception as e:
                logger.error(f"窗口大小 {window_size} 的固定窗口规则处理失败: {str(e)}")
                continue

        logger.info(f"固定窗口处理完成，总计产生 {len(total_format_alerts)} 个新告警，{len(total_update_alerts)} 个更新")

        return self._execute_processing(total_format_alerts, total_update_alerts)


class SessionWindowAggProcessor(BaseWindowProcessor):
    """会话窗口聚合处理器

    会话窗口的核心理念：基于事件活动检测"活动停止"状态
    
    处理流程：
    1. **规则过滤阶段**：使用关联规则过滤事件，只处理符合业务条件的事件
       - 例如：只处理流水线AAAA构建失败的事件
       - 确保会话管理只关注相关的业务事件
    
    2. **会话管理阶段**：对符合条件的事件进行会话分组和生命周期管理
       - 会话开始：系统检测到第一个符合条件的事件（如第一次流水线失败）
       - 会话扩展：后续每个相关事件都会被纳入当前会话，并重置会话倒计时（基于Session Gap参数）
       - 会话结束：当超过Session Gap时间无新事件到达，或达到最大持续时间
    
    3. **告警生成阶段**：会话结束时根据条件触发告警
       - 例如：10分钟内没有继续操作的事件，意味着短时间内代码问题无法解决，触发告警
       - 告警触发链路保持和其他两个窗口类型一致
    
    关键特性：
    - 动态窗口大小：根据事件活动情况自动调整
    - 状态持久化：支持跨任务执行周期的会话管理
    - 活动检测：专门用于检测"无人处理"、"故障未恢复"等场景
    """

    def get_window_type(self) -> str:
        return "session"

    def process_rules(self, rules: List[CorrelationRules]) -> Tuple[int, int]:
        """
        会话窗口规则

        会话窗口处理逻辑：
        1.保持和其他两个窗口的逻辑
        2.创建Alert变成创建会话/更新会话里的Event
        3.检查超时的会话，若超时则结束会话并生成告警
        """
        logger.info(f"开始处理会话窗口规则，数量: {len(rules)}")

        # 按窗口大小分组规则
        grouped_rules = self._group_rules_by_window_size(rules)

        total_format_alerts = {}
        total_update_alerts = {}

        # 按窗口大小分组处理
        for window_size, size_rules in grouped_rules.items():
            logger.info(f"处理会话大小 {window_size} 的会话窗口规则，数量: {len(size_rules)}")

            try:
                # 为每个窗口大小创建专门的处理器
                processor = AlertProcessor(window_size=window_size)

                # 性能优化：只加载当前需要的规则
                processor.set_target_correlation_rules(size_rules)
                processor.reload_database_rules()

                # 批量处理该窗口大小的规则
                batch_alerts, batch_updates = processor._process_batch_correlation_rules(
                    size_rules, self.get_window_type()
                )
                if batch_updates:
                    total_update_alerts.update({i['fingerprint']: i for i in batch_updates})

                # 将告警转换为会话事件
                self._convert_alerts_to_session_events(batch_alerts, size_rules)

                # 检查并处理超时的会话，生成告警
                timeout_alerts, timeout_updates = self._process_timeout_sessions(size_rules)
                format_timout_alerts = [self.processor.format_event_to_alert(i) for i in timeout_alerts]

                total_format_alerts.update({i['fingerprint']: i for i in format_timout_alerts})
                total_update_alerts.update({i['fingerprint']: i for i in timeout_updates})

                logger.info(f"会话窗口大小 {window_size} 处理完成")

            except Exception as e:
                logger.error(f"会话窗口大小 {window_size} 的会话窗口规则处理失败: {str(e)}")
                continue

        logger.info(f"会话窗口处理完成，总计产生 {len(total_format_alerts)} 个新告警，{len(total_update_alerts)} 个更新")

        return self._execute_processing(list(total_format_alerts.values()), list(total_update_alerts.values()))

    def _convert_alerts_to_session_events(self, batch_alerts: List[Dict[str, Any]],
                                          correlation_rules: List[CorrelationRules]) -> Tuple[
        List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        将批量告警转换为会话事件
        
        Args:
            batch_alerts: 批量新告警列表
            correlation_rules: 关联规则列表
            
        Returns:
            Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: (新建告警数据, 更新告警数据)
        """

        logger.info(f"开始转换 {len(batch_alerts)} 个新告警为会话事件")

        current_time = self.now
        session_created_count = 0
        session_updated_count = 0

        try:
            with transaction.atomic():
                # 处理所有告警（新建+更新）
                all_alerts = batch_alerts

                for alert_data in all_alerts:
                    events = alert_data.get('events', [])
                    if not events:
                        continue

                    # 为每个关联规则处理会话
                    for correlation_rule in correlation_rules:
                        session_key = self._generate_session_key_for_alert(alert_data)

                        # 查找或创建会话
                        session = self._get_or_create_session_for_rule(
                            session_key, alert_data, correlation_rule, current_time
                        )

                        if session:
                            # 将事件添加到会话中
                            added_count = self._add_events_to_session(session, events)
                            if added_count > 0:
                                # 通过判断会话中事件的总数来确定是新建还是更新
                                current_event_count = session.events.count()
                                if current_event_count == added_count:
                                    session_created_count += 1
                                else:
                                    session_updated_count += 1

                                logger.debug(f"会话 {session.session_id} 添加了 {added_count} 个事件")

        except Exception as e:
            logger.error(f"转换告警为会话事件失败: {str(e)}")

        logger.info(f"会话事件转换完成: 创建 {session_created_count} 个会话, 更新 {session_updated_count} 个会话")

        # 不返回告警数据，因为我们现在只是在管理会话，真正的告警将在超时检查中生成
        return [], []

    @staticmethod
    def _generate_session_key_for_alert(alert_data: Dict[str, Any]) -> str:
        """
        为告警数据生成会话键
        
        Args:
            alert_data: 告警数据

        Returns:
            str: 会话键
        """
        session_key_fields = "session-{}".format(alert_data['fingerprint'])
        return session_key_fields

    @staticmethod
    def _get_or_create_session_for_rule(session_key: str, alert_data: Dict[str, Any],
                                        correlation_rule: CorrelationRules, current_time) -> SessionWindow | None:
        """
        为规则获取或创建会话
        
        Args:
            session_key: 会话键
            alert_data: 告警数据
            correlation_rule: 关联规则
            current_time: 当前时间
            
        Returns:
            SessionWindow: 会话实例
        """

        try:
            rule_id = correlation_rule.rule_id_str
            alert_events = alert_data.get('events', [])
            if not alert_events:
                return

            # 查找活跃的会话
            active_session = SessionWindow.objects.filter(
                session_key=session_key,
                rule_id=rule_id,
                events__in=alert_events
            ).first()

            # 判断event是不是成功的 成功的话就不进行会话创建
            if active_session:
                # 尝试扩展现有会话
                if active_session.check_has_events(alert_events):
                    return active_session
                if active_session.extend_session(current_time, alert_events):
                    return active_session
                else:
                    # 会话已过期，需要创建新会话
                    logger.info(f"会话 {active_session.session_id} 已过期，创建新会话")

            # 创建新会话
            session_timeout_seconds = int(
                WindowCalculator.parse_time_str(correlation_rule.session_timeout).total_seconds()
            )

            session = SessionWindow.objects.create(
                session_id=f"SESSION-{uuid.uuid4().hex[:8].upper()}",
                session_key=session_key,
                rule_id=rule_id,
                session_start=current_time,
                last_activity=current_time,
                session_timeout=session_timeout_seconds,
                is_active=True,
                session_data={
                    'created_by_rule': correlation_rule.name,
                    'alert_fingerprint': alert_data.get('fingerprint'),
                    'window_config': {
                        'session_timeout': correlation_rule.session_timeout,
                        'max_window_size': correlation_rule.max_window_size,
                        'session_key_fields': correlation_rule.session_key_fields
                    }
                }
            )

            logger.info(f"创建新会话: {session.session_id}, 规则: {correlation_rule.name}")
            return session

        except Exception as e:
            import traceback
            logger.error(f"获取或创建会话失败: {traceback.format_exc()}")
            return None

    def _add_events_to_session(self, session: SessionWindow, events) -> int:
        """
        将事件添加到会话中

        Args:
            session: 会话实例
            events: Event 模型的 QuerySet 或 事件列表

        Returns:
            int: 成功添加的事件数量
        """
        added_count = 0

        try:
            # 确保 events 是可迭代的（支持 QuerySet 和 list）
            if hasattr(events, 'all'):
                # 如果是 QuerySet，转换为列表以避免重复查询
                event_list = list(events.all())
            else:
                # 如果已经是列表，直接使用
                event_list = list(events)

            if not event_list:
                return 0

            # 批量检查已存在的事件关联，提高性能
            existing_event_ids = set(
                SessionEventRelation.objects.filter(
                    session=session,
                    event__in=event_list  # 使用event_id字段进行查询
                ).values_list('event_id', flat=True)
            )

            # 准备批量创建的关联关系列表
            relations_to_create = []

            for event in event_list:
                # 获取事件ID
                event_id = event.id
                if not event_id:
                    continue

                # 跳过已存在的事件关联
                if event_id in existing_event_ids:
                    logger.debug(f"事件 {event_id} 已存在于会话 {session.session_id} 中，跳过")
                    continue

                # 准备创建新的关联关系
                relations_to_create.append(
                    SessionEventRelation(
                        session=session,
                        event=event
                    )
                )
                added_count += 1

            # 批量创建关联关系，提高数据库操作效率
            if relations_to_create:
                try:
                    # 使用 ignore_conflicts=True 避免重复插入错误
                    created_relations = SessionEventRelation.objects.bulk_create(
                        relations_to_create,
                        batch_size=1000,  # Django 建议的批量创建大小
                        ignore_conflicts=True  # 忽略唯一性约束冲突
                    )
                    actual_added_count = len(created_relations)
                    # 更新会话的最后活动时间
                    if actual_added_count > 0:
                        session.last_activity = self.now
                        session.save(update_fields=['last_activity', 'updated_at'])

                        logger.debug(f"成功为会话 {session.session_id} 添加了 {actual_added_count} 个事件")

                    added_count = actual_added_count

                except Exception as bulk_create_error:
                    logger.error(f"批量创建会话事件关联失败: {str(bulk_create_error)}", exc_info=True)
                    # 如果批量创建失败，尝试逐个创建
                    added_count = self._add_events_individually(session, relations_to_create)

        except Exception as e:
            logger.error(f"添加事件到会话失败: {str(e)}", exc_info=True)
            # 发生异常时回滚 added_count
            added_count = 0

        return added_count

    def _add_events_individually(self, session: SessionWindow, relations_to_create: list) -> int:
        """
        逐个添加事件关联关系（批量创建失败时的备用方案）

        Args:
            session: 会话实例
            relations_to_create: 要创建的关联关系列表

        Returns:
            int: 成功添加的事件数量
        """
        added_count = 0

        for relation in relations_to_create:
            try:
                # 使用 get_or_create 避免重复插入
                session_relation, created = SessionEventRelation.objects.get_or_create(
                    session=session,
                    event=relation.event
                )

                if created:
                    added_count += 1
                    logger.debug(f"成功添加事件 {relation.event.event_id} 到会话 {session.session_id}")
                else:
                    logger.debug(f"事件 {relation.event.event_id} 已存在于会话 {session.session_id}")

            except Exception as e:
                logger.warning(f"添加单个事件关联失败: {str(e)}")
                continue

        # 更新会话统计
        if added_count > 0:
            session.last_activity = self.now
            session.save(update_fields=['last_activity', 'updated_at'])

        return added_count

    def _process_timeout_sessions(self, correlation_rules: List[CorrelationRules]) -> Tuple[
        List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        处理超时的会话，生成告警
        
        Args:
            correlation_rules: 关联规则列表
            
        Returns:
            Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: (新建告警数据, 更新告警数据)
        """

        timeout_alerts = []
        timeout_updates = []

        try:
            for correlation_rule in correlation_rules:
                rule_id = correlation_rule.rule_id_str

                # 获取该规则的所有活跃会话
                active_sessions = SessionWindow.objects.filter(
                    rule_id=rule_id,
                    is_active=True
                ).prefetch_related('events')

                for session in active_sessions:
                    should_close, reason = session.should_close_window(self.now)

                    if should_close:
                        # 会话超时，生成告警数据
                        create_data, update_data = self._create_alert_data_from_session(session, correlation_rule)

                        if create_data:
                            timeout_alerts.extend(create_data)
                        if update_data:
                            timeout_updates.extend(update_data)

                        # 关闭会话
                        session.is_active = False
                        session.session_data['close_reason'] = reason
                        session.session_data['close_time'] = self.now.isoformat()
                        session.save(update_fields=['is_active', 'session_data', 'updated_at'])

                        logger.info(f"会话 {session.session_id} 超时关闭，生成告警，原因: {reason}")

        except Exception as e:
            logger.error(f"处理超时会话失败: {str(e)}")

        return timeout_alerts, timeout_updates

    def _create_alert_data_from_session(self, session: SessionWindow, correlation_rule: CorrelationRules) -> tuple[
        list, list]:
        """
        从会话创建告警数据
        
        Args:
            session: 会话实例
            correlation_rule: 关联规则
            
        Returns:
            Dict[str, Any]: 告警数据
        """
        create_data = []
        update_data = []

        try:
            # 获取会话中的所有事件
            session_events = list(
                session.events.all().select_related("source").values(*self.fields).order_by('received_at'))

            if not session_events:
                return create_data, update_data

            # 获取关联的聚合规则（取第一个作为基础）
            aggregation_rule = correlation_rule.aggregation_rules.filter(is_active=True).first()
            if not aggregation_rule:
                return create_data, update_data

            aggregation_key = self.processor.rule_manager.get_aggregation_key(aggregation_rule.rule_id)

            event_map = {}
            for session_event in session_events:
                session_event["alert_source"] = session_event["source__name"]
                fingerprint = generate_instance_fingerprint(session_event, fields=aggregation_key)
                event_map.setdefault(fingerprint, []).append(session_event)

            for _fingerprint, event_data in event_map.items():
                if not event_data:
                    continue
                # 基于第一个事件创建告警基础数据
                first_event = event_data[0]
                query_conditions = {
                    'status__in': AlertStatus.ACTIVATE_STATUS,
                    'fingerprint': _fingerprint,  # 使用实例指纹查询
                    'rule_id': aggregation_rule.rule_id
                }
                related_alerts = list(Alert.objects.filter(**query_conditions).values())
                # 创建告警数据
                alert_data = {
                    "source_name": first_event["alert_source"],
                    "rule_name": aggregation_rule.rule_id,
                    "description": first_event.get("description", ""),
                    "severity": aggregation_rule.severity,
                    "event_data": event_data,
                    "event_ids": [i["event_id"] for i in event_data],
                    "created_at": self.now,
                    "rule": aggregation_rule,
                    "fingerprint": _fingerprint,
                    "related_alerts": related_alerts,
                    "rule_id": aggregation_rule.rule_id
                }
                if related_alerts:
                    update_data.append(alert_data)
                else:
                    create_data.append(alert_data)

        except Exception as e:
            logger.error(f"从会话创建告警数据失败: {str(e)}")
            return [], []

        return create_data, update_data


class WindowProcessorFactory:
    """窗口处理器工厂类"""

    _processors = {
        'sliding': SlidingWindowProcessor,
        'fixed': FixedWindowProcessor,
        'session': SessionWindowAggProcessor  # 修复：使用重命名的类
    }

    @classmethod
    def create_processor(cls, window_type: str, window_size: str = "10min") -> BaseWindowProcessor:
        """
        创建窗口处理器实例
        
        Args:
            window_type: 窗口类型 (sliding/fixed/session)
            window_size: 窗口大小（仅用于初始化，实际处理时会根据规则动态调整）
            
        Returns:
            窗口处理器实例
            
        Raises:
            ValueError: 不支持的窗口类型
        """
        if window_type not in cls._processors:
            raise ValueError(f"不支持的窗口类型: {window_type}")

        processor_class = cls._processors[window_type]
        return processor_class(window_size=window_size)

    @classmethod
    def get_supported_window_types(cls) -> List[str]:
        """获取支持的窗口类型列表"""
        return list(cls._processors.keys())

    @classmethod
    def process_window_type_rules(cls, window_type: str, rules: List[CorrelationRules]) -> Tuple[int, int]:
        """
        便捷方法：直接处理指定窗口类型的规则
        
        Args:
            window_type: 窗口类型
            rules: 规则列表（每个规则有自己的窗口大小配置）
            
        Returns:
            Tuple[int, int]: (新建告警数, 更新告警数)
        """
        # 创建处理器时使用默认窗口大小，实际处理时会根据每个规则的配置动态调整
        processor = cls.create_processor(window_type)
        return processor.process_rules(rules)
