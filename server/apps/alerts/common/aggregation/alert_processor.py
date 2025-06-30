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
from apps.alerts.common.rules.rule_manager import get_rule_manager
from apps.alerts.common.rules.alert_rules import format_alert_message
from apps.alerts.constants import AlertStatus, LevelType, EventStatus
from apps.alerts.models import Event, Alert, Level
from apps.core.logger import alert_logger as logger


class AlertProcessor:
    def __init__(self, window_size: str = "10min"):
        self.window_size = window_size
        # 获取支持数据库规则的规则管理器
        self.rule_manager = get_rule_manager(window_size=self.window_size)
        self.event_fields = [
            "event_id", "external_id", "item", "received_at", "status", "level", "source__name",
            "source_id", "title", "rule_id", "description", "resource_id", "resource_type", "resource_name", "value"
        ]
        self.now = timezone.now()
        # 定义级别优先级映射（数字越大优先级越高）
        self.level_priority = self._get_event_level_list()

    @staticmethod
    def _get_event_level_list():
        """获取事件级别映射"""
        instance = list(
            Level.objects.filter(level_type=LevelType.EVENT, level_id__lt=3).order_by("level_id").values_list(
                "level_id", flat=True))
        return instance

    def get_events(self) -> pd.DataFrame:
        """获取事件数据"""
        get_time = int(self.window_size.split("min")[0])
        start_time = self.now - datetime.timedelta(minutes=get_time)
        instances = Event.objects.filter(
            received_at__gte=start_time,
            received_at__lt=self.now,
            source__is_active=True,
        ).exclude(status=EventStatus.SHIELD).values(*self.event_fields)
        return pd.DataFrame(list(instances))

    def process(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """处理主流程"""
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
            "first_event_time": _instances.last().received_at,
            "last_event_time": _instances.first().received_at,
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

    def add_custom_rule(self, rule_config: Dict[str, Any]) -> bool:
        """添加自定义规则"""
        return self.rule_manager.add_rule(rule_config)

    def update_rule(self, rule_name: str, rule_config: Dict[str, Any]) -> bool:
        """更新规则"""
        return self.rule_manager.update_rule(rule_name, rule_config)

    def remove_rule(self, rule_name: str) -> bool:
        """删除规则"""
        return self.rule_manager.remove_rule(rule_name)

    def reload_rules(self):
        """重新加载规则"""
        self.rule_manager.reload_rules()

    def reload_database_rules(self):
        """重新加载数据库规则"""
        try:
            self.rule_manager.reload_rules_from_database()
            logger.info("告警处理器成功重新加载数据库规则")
        except Exception as e:
            logger.error(f"告警处理器重新加载数据库规则失败: {str(e)}")

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
