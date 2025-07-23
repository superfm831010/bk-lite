# -- coding: utf-8 --
# @File: alert_processor.py
# @Time: 2025/5/21 11:03
# @Author: windyzhao
import uuid

import pandas as pd
import datetime
from typing import List, Dict, Any, Tuple

from django.db import transaction, IntegrityError
from django.utils import timezone

from apps.alerts.common.assignment import execute_auto_assignment_for_alerts
from apps.alerts.common.rules.db_rule_manager import DatabaseRuleManager
from apps.alerts.common.rules.rule_manager import get_rule_manager
from apps.alerts.common.rules.alert_rules import format_alert_message
from apps.alerts.constants import AlertStatus, LevelType, EventStatus
from apps.alerts.common.aggregation.window_types import WindowType, WindowConfig, WindowCalculator
from apps.alerts.models import Event, Alert, Level, AggregationRules, CorrelationRules, SessionWindow
from apps.alerts.utils.util import generate_instance_fingerprint
from apps.core.logger import alert_logger as logger


class AlertProcessor:
    def __init__(self, window_size: str = "10min", window_type: str = "sliding"):
        """
        初始化告警处理器
        
        Args:
            window_size: 默认窗口大小，如"10min"（用于向后兼容）
            window_type: 默认窗口类型，支持 sliding/fixed/session（用于向后兼容）
        """
        self.default_window_size = window_size
        self.default_window_type = WindowType(window_type)

        # 获取支持数据库规则的规则管理器
        self.rule_manager = get_rule_manager(window_size=self.default_window_size)

        self.event_fields = [
            "event_id", "external_id", "item", "received_at", "status", "level", "source__name",
            "source_id", "title", "rule_id", "description", "resource_id", "resource_type", "resource_name", "value"
        ]
        self.now = timezone.now()
        # 定义级别优先级映射（数字越大优先级越高）
        self.level_priority = self._get_event_level_list()

        # 新增：支持只处理特定规则，避免重复加载
        self._target_correlation_rules = None
        self._rule_manager_initialized = False

    @staticmethod
    def _get_event_level_list():
        """获取事件级别映射"""
        instance = list(
            Level.objects.filter(level_type=LevelType.EVENT, level_id__lt=3).order_by("level_id").values_list(
                "level_id", flat=True))
        return instance

    def get_events_for_correlation_rule(self, correlation_rule: CorrelationRules) -> pd.DataFrame:
        """根据关联规则的窗口配置获取事件数据"""
        # 根据窗口类型确定查询时间范围
        if correlation_rule.window_type == 'sliding':
            # 滑动窗口：查询窗口大小内的数据
            window_delta = WindowCalculator.parse_time_str(correlation_rule.window_size)
            start_time = self.now - window_delta
        elif correlation_rule.window_type == 'fixed':
            # 固定窗口：查询足够大的范围以支持对齐计算
            window_delta = WindowCalculator.parse_time_str(correlation_rule.window_size)
            # 为固定窗口预留更多数据，确保对齐计算正确
            start_time = self.now - window_delta * 2
        elif correlation_rule.window_type == 'session':
            # 会话窗口：查询更大的范围以支持会话分析
            max_window = WindowCalculator.parse_time_str(self.default_window_size)
            start_time = self.now - max_window
        else:
            # 默认使用滑动窗口逻辑
            window_delta = WindowCalculator.parse_time_str(correlation_rule.window_size)
            start_time = self.now - window_delta

        instances = Event.objects.filter(
            received_at__gte=start_time,
            received_at__lt=self.now,
            source__is_active=True
        ).exclude(status=EventStatus.SHIELD, alert__status__in=AlertStatus.ACTIVATE_STATUS).values(*self.event_fields)

        return pd.DataFrame(list(instances))

    def get_events(self, rule_config: WindowConfig = None) -> pd.DataFrame:
        """向后兼容的事件获取方法"""
        if rule_config and rule_config.window_type != WindowType.SLIDING:
            # 非滑动窗口需要更大的查询范围以支持窗口计算
            max_window = WindowCalculator.parse_time_str(rule_config.max_window_size)
            start_time = self.now - max_window
        else:
            # 滑动窗口使用原有逻辑
            get_time = int(self.default_window_size.split("min")[0])
            start_time = self.now - datetime.timedelta(minutes=get_time)

        instances = Event.objects.filter(
            received_at__gte=start_time,
            received_at__lt=self.now,
            source__is_active=True,
        ).exclude(status=EventStatus.SHIELD).values(*self.event_fields)
        return pd.DataFrame(list(instances))

    def process(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """处理主流程 - 支持多种窗口类型"""
        # 检查是否启用多窗口类型处理
        if self._should_use_multi_window_processing():
            logger.info("使用多窗口类型处理模式")
            return self.process_with_window_type()
        else:
            logger.info("使用传统滑动窗口处理模式")
            return self._process_legacy_sliding_window()

    def _should_use_multi_window_processing(self) -> bool:
        """判断是否需要使用多窗口类型处理
        
        检查是否有非滑动窗口类型的关联规则
        """
        try:
            non_sliding_rules = CorrelationRules.objects.filter(
                aggregation_rules__is_active=True
            ).exclude(window_type='sliding').exists()

            return non_sliding_rules
        except Exception as e:
            logger.warning(f"检查窗口类型失败，使用传统模式: {e}")
            return False

    def _process_legacy_sliding_window(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """传统滑动窗口处理逻辑（向后兼容）"""
        format_alert_list = []
        update_alert_list = []
        try:
            # 1. 获取事件数据
            events = self.get_events()

            # 2. 使用规则管理器执行规则检测
            logger.info("==start process events with rule manager==")
            rule_results = self.rule_manager.execute_rules(events)
            logger.info("==end process events with rule manager==")

            # 3. 处理规则执行结果
            for rule_id, rule_result in rule_results.items():
                if rule_result.triggered:
                    rule_config = self.rule_manager.get_rule_by_id(rule_id)
                    if not rule_config:
                        logger.warning(f"Rule config not found for: {rule_id}")
                        continue

                    # 根据event_id拿出event的原始数据
                    for fingerprint, _event_dict in rule_result.instances.items():
                        event_ids = _event_dict['event_ids']  # 事件ID列表
                        event_data = events[events['event_id'].isin(event_ids)].to_dict('records')
                        related_alerts = _event_dict.get("related_alerts", [])

                        alert = {
                            "rule_name": rule_id,
                            "description": rule_result.description,
                            "severity": rule_result.severity,
                            "event_data": event_data,
                            "event_ids": event_ids,
                            "created_at": self.now,
                            "rule": rule_config,
                            "source_name": rule_result.source_name,
                            "fingerprint": fingerprint,
                            "related_alerts": related_alerts,
                            "rule_id": rule_id
                        }

                        if related_alerts:
                            # 更新告警
                            update_alert_list.append(alert)
                        else:
                            # 保存告警数据
                            format_alert = self.format_event_to_alert(alert)
                            format_alert_list.append(format_alert)

            return format_alert_list, update_alert_list
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            return [], []

    def get_max_level(self, event_levels):
        # 对于高等级事件聚合规则，取最低等级（数字最小）
        # 对于其他规则，取最高等级（数字最小）
        logger.debug(f"Processing event levels: {event_levels}")
        event_levels = [int(i) for i in event_levels]
        highest_level = min(event_levels)
        if highest_level not in self.level_priority:
            highest_level = self.level_priority[-1]
        return int(highest_level)

    def get_min_level(self, event_levels):
        logger.debug(f"Processing event levels: {event_levels}")
        event_levels = [int(i) for i in event_levels]
        low_level = max(event_levels)
        if low_level not in self.level_priority:
            low_level = self.level_priority[-1]
        return int(low_level)

    def _get_level_for_aggregation_rule(self, rule_name: str, event_levels):
        """根据规则类型获取告警等级"""
        if rule_name == "high_level_event_aggregation":
            # 高等级事件聚合：取最低等级作为告警等级
            return max(event_levels) if event_levels else self.level_priority[-1]
        else:
            # 其他规则：取最高等级
            return self.get_max_level(event_levels)

    def format_event_to_alert(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """格式化事件数据为告警数据"""
        events = params["event_data"]
        event_ids = params["event_ids"]
        rule = params["rule"]
        rule_name = params["rule_name"]
        source_name = params["source_name"]
        rule_id = params["rule_id"]
        _instances, level = self.get_event_instances(event_ids=event_ids, level_max=False)

        # 根据规则类型调整等级获取逻辑
        event_levels = set(_instances.values_list('level', flat=True))
        if rule_name in ["high_level_event_aggregation"]:
            level = self.get_max_level(list(event_levels))

        base_event = events[0]  # 取第一个事件作为基础事件
        title, content = format_alert_message(rule=rule, event_data=base_event)
        alert = {
            "alert_id": f"ALERT-{uuid.uuid4().hex.upper()}",
            "level": level,
            "title": title,
            "content": content,
            "item": base_event["item"],
            "resource_id": base_event["resource_id"],
            "resource_name": base_event["resource_name"],
            "resource_type": base_event["resource_type"],
            "first_event_time": _instances.first().received_at,
            "last_event_time": _instances.last().received_at,
            "events": _instances,
            "source_name": source_name,
            "fingerprint": params["fingerprint"],
            "rule_id": rule_id
        }

        return alert

    def get_event_instances(self, event_ids: List[str], level_max: bool = True):
        """根据事件ID获取事件实例"""

        instances = Event.objects.filter(event_id__in=event_ids).order_by("received_at")

        # 获取所有事件的级别
        event_levels = set(instances.values_list('level', flat=True))

        # 根据优先级排序找出最高级别
        if level_max:
            level = self.get_max_level(event_levels)
        else:
            level = self.get_min_level(event_levels)

        return instances, level

    def bulk_create_alerts(self, alerts: List[Dict[str, Any]]) -> List[str]:
        """批量创建告警"""

        result = []

        if not alerts:
            return result

        with transaction.atomic():
            for alert in alerts:
                try:
                    events = alert.pop("events")
                    fingerprint = alert.get("fingerprint")

                    # 使用 select_for_update 防止并发问题
                    existing_active_alert = Alert.objects.select_for_update().filter(
                        fingerprint=fingerprint,
                        status__in=AlertStatus.ACTIVATE_STATUS
                    ).first()

                    if existing_active_alert:
                        # 已有活跃告警，更新它
                        existing_active_alert.level = self.get_max_level(
                            [int(existing_active_alert.level), int(alert['level'])])
                        existing_active_alert.last_event_time = alert.get('last_event_time',
                                                                          existing_active_alert.last_event_time)
                        existing_active_alert.save(update_fields=['level', 'last_event_time'])
                        existing_active_alert.events.add(*events)
                        logger.info(f"Updated existing alert with fingerprint: {fingerprint}")
                    else:
                        # 没有活跃告警，创建新的
                        try:
                            # TODO 告警状态 匹配不到处理人为未分派其余的，匹配到就是待响应
                            alert_obj = Alert.objects.create(**alert)
                            through_model = Alert.events.through
                            through_values = [
                                through_model(alert_id=alert_obj.id, event_id=event.id)
                                for event in events
                            ]
                            through_model.objects.bulk_create(through_values)
                            logger.info(f"Created new alert with fingerprint: {fingerprint}")
                            result.append(alert_obj.alert_id)
                        except IntegrityError:
                            # 如果有唯一约束冲突，重新查询并更新
                            existing_alert = Alert.objects.filter(
                                fingerprint=fingerprint,
                                status__in=AlertStatus.ACTIVATE_STATUS
                            ).first()
                            if existing_alert:
                                existing_alert.events.add(*events)
                                logger.info(f"Found concurrent alert, updated instead: {fingerprint}")

                except Exception as err:
                    import traceback
                    logger.error("Error processing alert: {}".format(traceback.format_exc()))

        return result

    def update_alerts(self, alerts: List[Dict[str, Any]]) -> None:
        """
        更新告警数据 - get_or_create版本
        """
        bulk_data = []
        with transaction.atomic():
            for alert_dict in alerts:
                event_ids = alert_dict["event_ids"]
                fingerprint = alert_dict["fingerprint"]
                try:
                    # 查找活跃告警
                    active_alerts = Alert.objects.select_for_update().filter(
                        fingerprint=fingerprint,
                        status__in=AlertStatus.ACTIVATE_STATUS
                    )
                    if active_alerts.exists():
                        # 更新现有活跃告警
                        alert_obj = active_alerts.first()
                        instances, level = self.get_event_instances(event_ids=event_ids, level_max=False)
                        last_event_time = instances.last().received_at
                        # alert_obj.level = self.get_max_level([int(alert_obj.level), level])
                        alert_obj.level = self.get_min_level([int(alert_obj.level), level])
                        alert_obj.last_event_time = last_event_time
                        alert_obj.save(update_fields=['level', 'last_event_time'])
                        alert_obj.events.add(*instances)
                        logger.info(f"Updated existing active alert: {fingerprint}")
                    else:
                        format_alert = self.format_event_to_alert(alert_dict)
                        bulk_data.append(format_alert)
                        self.bulk_create_alerts(bulk_data)

                except Exception as err:
                    import traceback
                    logger.error(f"Error updating alert {fingerprint}: {traceback.format_exc()}")

    def get_rule_statistics(self) -> Dict[str, Any]:
        """获取规则统计信息"""
        return self.rule_manager.get_rule_statistics()

    def reload_rules(self):
        """重新加载规则"""
        self.rule_manager.reload_rules()

    def reload_database_rules(self):
        """重新加载数据库规则"""
        try:
            if self._target_correlation_rules:
                # 只加载目标关联规则
                self._load_specific_correlation_rules(self._target_correlation_rules)
            else:
                # 加载所有规则
                self.rule_manager.reload_rules_from_database()

            self._rule_manager_initialized = True
            logger.info("告警处理器成功重新加载数据库规则")
        except Exception as e:
            logger.error(f"告警处理器重新加载数据库规则失败: {str(e)}")

    def set_target_correlation_rules(self, correlation_rules: List[CorrelationRules]):
        """
        设置目标关联规则，只处理这些规则
        
        Args:
            correlation_rules: 要处理的关联规则列表
        """
        self._target_correlation_rules = correlation_rules
        self._rule_manager_initialized = False

    def _load_specific_correlation_rules(self, correlation_rules: List[CorrelationRules]):
        """
        只加载特定的关联规则到规则管理器
        
        Args:
            correlation_rules: 要加载的关联规则列表
        """
        try:
            logger.info(f"开始加载特定的关联规则，数量: {len(correlation_rules)}")

            # 创建专门的数据库规则管理器来处理特定规则
            db_rule_manager = DatabaseRuleManager(window_size=self.default_window_size)

            # 直接获取窗口配置对象
            window_config = db_rule_manager.load_specific_correlation_rules(correlation_rules)

            if window_config:
                # 更新规则管理器的配置
                self.rule_manager.window_config = window_config
                self.rule_manager._init_engine()

                total_rules = len(window_config.rules) if window_config.rules else 0
                logger.info(f"成功加载 {total_rules} 条特定规则，窗口类型: {window_config.window_type}")
            else:
                logger.warning("加载的特定规则为空")

        except Exception as e:
            logger.error(f"加载特定关联规则失败: {str(e)}")
            raise

    def _ensure_rule_manager_initialized(self):
        """确保规则管理器已初始化"""
        if not self._rule_manager_initialized:
            self.reload_database_rules()

    @staticmethod
    def alert_auto_assign(alert_id_list) -> None:
        """
        自动分配告警处理人
        """
        try:
            execute_auto_assignment_for_alerts(alert_id_list)
        except Exception as err:
            import traceback
            logger.error(f"Error in auto assignment for alerts {alert_id_list}: {traceback.format_exc()}")

    def process_with_window_type(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """根据关联规则的窗口类型进行分组处理"""
        format_alert_list = []
        update_alert_list = []

        try:
            # 获取所有激活的关联规则，按窗口类型分组
            active_correlation_rules = self._get_active_correlation_rules_by_window_type()

            if not active_correlation_rules:
                logger.info("没有发现激活的关联规则")
                return [], []

            # 按窗口类型分别处理
            for window_type, correlation_rules in active_correlation_rules.items():
                logger.info(f"处理窗口类型: {window_type}, 关联规则数量: {len(correlation_rules)}")

                # 根据窗口类型选择处理策略
                if window_type == 'session':
                    # 会话窗口：每个关联规则单独处理
                    for correlation_rule in correlation_rules:
                        session_alerts, session_updates = self._process_session_correlation_rule(correlation_rule)
                        format_alert_list.extend(session_alerts)
                        update_alert_list.extend(session_updates)
                else:
                    # 滑动窗口和固定窗口：可以批量处理
                    batch_alerts, batch_updates = self._process_batch_correlation_rules(correlation_rules, window_type)
                    format_alert_list.extend(batch_alerts)
                    update_alert_list.extend(batch_updates)

        except Exception as e:
            logger.error(f"多窗口类型处理失败: {str(e)}", exc_info=True)

        return format_alert_list, update_alert_list

    def _get_active_correlation_rules_by_window_type(self) -> Dict[str, List[CorrelationRules]]:
        """获取按窗口类型分组的激活关联规则"""
        # 获取所有激活的关联规则
        active_correlation_rules = CorrelationRules.objects.filter(
            aggregation_rules__is_active=True
        ).prefetch_related('aggregation_rules').distinct()

        # 按窗口类型分组
        rules_by_window_type = {}
        for correlation_rule in active_correlation_rules:
            window_type = correlation_rule.window_type
            if window_type not in rules_by_window_type:
                rules_by_window_type[window_type] = []
            rules_by_window_type[window_type].append(correlation_rule)

        return rules_by_window_type

    def _process_session_correlation_rule(self, correlation_rule: CorrelationRules) -> Tuple[
        List[Dict[str, Any]], List[Dict[str, Any]]]:
        """处理单个会话窗口关联规则"""
        format_alert_list = []
        update_alert_list = []

        try:
            # 获取该关联规则的聚合规则
            aggregation_rules = correlation_rule.aggregation_rules.filter(is_active=True)
            if not aggregation_rules.exists():
                return [], []

            # 获取事件数据
            events = self.get_events_for_correlation_rule(correlation_rule)
            if events.empty:
                return [], []

            # 创建窗口配置
            config = self._create_window_config(correlation_rule)

            # 为每个聚合规则单独处理会话
            for aggregation_rule in aggregation_rules:
                session_results = self._process_session_window(events, config, aggregation_rule.rule_id)

                # 处理每个会话的事件
                for session_id, session_events in session_results:
                    if not session_events.empty:
                        # 为单个聚合规则处理会话事件
                        session_alerts, session_updates = self._process_events_with_aggregation_rules(
                            session_events, [aggregation_rule]
                        )
                        format_alert_list.extend(session_alerts)
                        update_alert_list.extend(session_updates)

                        logger.info(
                            f"会话 {session_id} 产生告警: {len(session_alerts)} 个新告警, {len(session_updates)} 个更新")

        except Exception as e:
            logger.error(f"处理会话窗口关联规则失败: {correlation_rule.name} - {str(e)}")

        return format_alert_list, update_alert_list

    def _create_window_config(self, correlation_rule: CorrelationRules) -> WindowConfig:
        """根据关联规则创建窗口配置"""
        from apps.alerts.common.aggregation.window_types import WindowConfig, WindowType

        return WindowConfig(
            window_type=WindowType(correlation_rule.window_type),
            window_size=correlation_rule.window_size,
            slide_interval=correlation_rule.slide_interval,
            alignment=correlation_rule.alignment,
            session_timeout=correlation_rule.session_timeout,
            session_key_fields=correlation_rule.session_key_fields or ['item', 'resource_id', 'resource_type',
                                                                       'alert_source', 'rule_id'],
            max_window_size=correlation_rule.max_window_size or "1h"
        )

    def main(self):
        """主流程方法"""
        add_alert_list, update_alert_list = self.process()
        logger.info("==add_alert_list data={}==".format([i.get("event_ids") for i in add_alert_list]))
        logger.info("==update_alert_list data={}==".format([i.get("event_ids") for i in update_alert_list]))
        if add_alert_list:
            self.bulk_create_alerts(alerts=add_alert_list)
            self.alert_auto_assign(alert_id_list=[alert['alert_id'] for alert in add_alert_list])

        if update_alert_list:
            self.update_alerts(alerts=update_alert_list)

    def _process_events_with_aggregation_rules(self, events: pd.DataFrame,
                                               aggregation_rules: List[AggregationRules]) -> Tuple[
        List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        使用聚合规则处理事件
        
        Args:
            events: 事件数据
            aggregation_rules: 聚合规则列表
            
        Returns:
            Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: (新建告警列表, 更新告警列表)
        """
        format_alert_list = []
        update_alert_list = []

        try:

            # 使用规则管理器执行规则检测
            rule_results = self.rule_manager.execute_rules(events)

            # 处理规则执行结果
            for rule_id, rule_result in rule_results.items():
                if rule_result.triggered:
                    # 检查规则是否在要处理的聚合规则列表中
                    matching_rule = None
                    for agg_rule in aggregation_rules:
                        if agg_rule.rule_id == rule_id:
                            matching_rule = agg_rule
                            break

                    if not matching_rule:
                        continue

                    rule_config = self.rule_manager.get_rule_by_id(rule_id)
                    if not rule_config:
                        logger.warning(f"Rule config not found for: {rule_id}")
                        continue

                    # 根据event_id拿出event的原始数据
                    for fingerprint, _event_dict in rule_result.instances.items():
                        event_ids = _event_dict['event_ids']
                        event_data = events[events['event_id'].isin(event_ids)].to_dict('records')
                        related_alerts = _event_dict.get("related_alerts", [])

                        alert = {
                            "rule_name": rule_id,
                            "description": rule_result.description,
                            "severity": rule_result.severity,
                            "event_data": event_data,
                            "event_ids": event_ids,
                            "created_at": self.now,
                            "rule": rule_config,
                            "source_name": rule_result.source_name,
                            "fingerprint": fingerprint,
                            "related_alerts": related_alerts,
                            "rule_id": rule_id
                        }

                        if related_alerts:
                            # 更新告警
                            update_alert_list.append(alert)
                        else:
                            # 保存告警数据
                            format_alert = self.format_event_to_alert(alert)
                            format_alert_list.append(format_alert)

        except Exception as e:
            logger.error(f"处理聚合规则失败: {str(e)}")

        return format_alert_list, update_alert_list

    def _process_batch_correlation_rules(self, correlation_rules: List[CorrelationRules], window_type: str) -> Tuple[
        List[Dict[str, Any]], List[Dict[str, Any]]]:
        """批量处理滑动窗口和固定窗口关联规则"""
        format_alert_list = []
        update_alert_list = []

        try:
            for correlation_rule in correlation_rules:
                # 获取该关联规则的聚合规则
                aggregation_rules = correlation_rule.aggregation_rules.filter(is_active=True)
                if not aggregation_rules.exists():
                    continue

                # 获取事件数据
                events = self.get_events_for_correlation_rule(correlation_rule)
                if events.empty:
                    continue

                # 检查是否需要处理会话关闭逻辑
                if correlation_rule.is_session_rule:
                    self._check_and_close_sessions_for_correlation_rule(correlation_rule, events)

                window_events = events

                if not window_events.empty:
                    window_alerts, window_updates = self._process_events_with_aggregation_rules(
                        window_events, list(aggregation_rules)
                    )
                    format_alert_list.extend(window_alerts)
                    update_alert_list.extend(window_updates)

                    logger.info(
                        f"关联规则 {correlation_rule.name} 产生告警: {len(window_alerts)} 个新告警, {len(window_updates)} 个更新")

        except Exception as e:
            logger.error(f"批量处理关联规则失败: {window_type} - {str(e)}")

        return format_alert_list, update_alert_list

    def _check_and_close_sessions_for_correlation_rule(self, correlation_rule: CorrelationRules, events: pd.DataFrame):
        """
        检查并关闭满足条件的会话

        Args:
            correlation_rule: 关联规则对象
            events: 当前批次的事件数据
        """

        try:
            current_time = self.now
            closed_sessions_count = 0

            # 获取该关联规则下所有活跃的会话
            active_sessions = SessionWindow.objects.filter(
                rule_id=correlation_rule.rule_id_str,
                is_active=True
            )

            if not active_sessions.exists():
                logger.debug(f"关联规则 {correlation_rule.name} 没有活跃的会话")
                return

            logger.info(f"开始检查关联规则 {correlation_rule.name} 的 {active_sessions.count()} 个活跃会话")

            # 获取聚合规则配置，用于检查会话关闭条件
            aggregation_rules = correlation_rule.aggregation_rules.filter(is_active=True)

            events['alert_source'] = events['source__name']
            # 生成实例指纹
            events['instance_fingerprint'] = events.apply(
                lambda row: generate_instance_fingerprint(row.to_dict()),
                axis=1
            )
            event_fingerprints = events.to_dict('records')
            event_fingerprints = {i["instance_fingerprint"]: i for i in event_fingerprints if i["value"] == 1}

            # 检查每个活跃会话
            for session in active_sessions:
                try:
                    # 2. 检查当前批次事件是否包含导致会话关闭的成功事件
                    session_key = session.session_key
                    # 从 session_key 中提取 fingerprint: "session-{fingerprint}" -> fingerprint
                    if session_key.startswith('session-'):
                        session_fingerprint = session_key.split("-", 1)[-1]  # 去掉 "session-" 前缀

                        # 检查是否有匹配的事件指纹
                        if session_fingerprint in event_fingerprints:
                            matching_events = event_fingerprints[session_fingerprint]

                            # 检查这些事件是否触发会话关闭条件
                            if self._should_close_session_by_events(session, matching_events, aggregation_rules):
                                self._close_session_with_reason(session, "success_event_received", current_time)
                                closed_sessions_count += 1

                except Exception as e:
                    logger.error(f"检查会话 {session.session_id} 关闭条件失败: {str(e)}")
                    continue

            if closed_sessions_count > 0:
                logger.info(f"关联规则 {correlation_rule.name} 共关闭了 {closed_sessions_count} 个会话")

        except Exception as e:
            logger.error(f"检查会话关闭条件失败: {str(e)}")

    def _should_close_session_by_events(self, session: 'SessionWindow', event: dict, aggregation_rules) -> bool:
        """
        检查事件是否触发会话关闭条件

        Args:
            session: 会话窗口对象
            events: 匹配会话的事件列表
            aggregation_rules: 聚合规则列表

        Returns:
            bool: 是否应该关闭会话
        """
        try:
            # 检查每个聚合规则的关闭条件
            for aggregation_rule in aggregation_rules:
                # 获取会话关闭条件配置
                session_close_conditions = aggregation_rule.get_session_close_conditions()

                if not session_close_conditions:
                    continue

                if self._match_session_close_condition(event, session_close_conditions):
                    logger.info(
                        f"会话 {session.session_id} 因事件匹配关闭条件而关闭: "
                        f"条件类型={session_close_conditions.get('type', 'unknown')}, "
                        f"事件={session_close_conditions.get('item', '')}={event.get('value', '')}"
                    )
                    return True

            return False

        except Exception as e:
            logger.error(f"检查事件关闭条件失败: {str(e)}")
            return False

    def _match_session_close_condition(self, event_data: Dict[str, Any], condition: Dict[str, Any]) -> bool:
        """
        检查事件是否匹配会话关闭条件

        Args:
            event_data: 事件数据
            condition: 关闭条件配置

        Returns:
            bool: 是否匹配
        """
        try:
            # 检查过滤条件
            filter_config = condition.get('filter', {})
            for filter_key, filter_value in filter_config.items():
                if event_data.get(filter_key) != filter_value:
                    return False

            # 检查目标字段和值
            target_field = condition.get('target_field')
            target_field_value = condition.get('target_field_value')
            target_value_field = condition.get('target_value_field')
            target_value = condition.get('target_value')
            operator = condition.get('operator', '==')

            # 检查目标字段值是否匹配
            if target_field and target_field_value is not None:
                if event_data.get(target_field) != target_field_value:
                    return False

            # 检查目标值是否匹配
            if target_value_field and target_value is not None:
                event_value = event_data.get(target_value_field)
                if not self._compare_values(event_value, target_value, operator):
                    return False

            return True

        except Exception as e:
            logger.error(f"检查关闭条件匹配失败: {str(e)}")
            return False

    def _compare_values(self, event_value, target_value, operator: str) -> bool:
        """
        比较事件值和目标值

        Args:
            event_value: 事件值
            target_value: 目标值
            operator: 比较操作符

        Returns:
            bool: 比较结果
        """
        try:
            if operator == '==':
                return event_value == target_value
            elif operator == '!=':
                return event_value != target_value
            elif operator == '>':
                return event_value > target_value
            elif operator == '>=':
                return event_value >= target_value
            elif operator == '<':
                return event_value < target_value
            elif operator == '<=':
                return event_value <= target_value
            else:
                logger.warning(f"未知的比较操作符: {operator}")
                return False

        except Exception as e:
            logger.error(f"比较值失败: {str(e)}")
            return False

    def _close_session_with_reason(self, session: 'SessionWindow', reason: str, close_time):
        """
        关闭会话并记录原因

        Args:
            session: 会话窗口对象
            reason: 关闭原因
            close_time: 关闭时间
        """
        try:
            with transaction.atomic():
                # 更新会话状态
                session.is_active = False
                session.session_data = session.session_data or {}
                session.session_data['close_reason'] = reason
                session.session_data['close_time'] = close_time.isoformat()
                session.session_data['closed_by'] = 'alert_processor'
                session.updated_at = close_time

                session.save(update_fields=['is_active', 'session_data', 'updated_at'])

                logger.info(f"会话 {session.session_id} 已关闭，原因: {reason}")

        except Exception as e:
            logger.error(f"关闭会话 {session.session_id} 失败: {str(e)}")
            raise
