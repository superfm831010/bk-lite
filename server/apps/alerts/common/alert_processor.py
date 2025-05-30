# -- coding: utf-8 --
# @File: alert_processor.py
# @Time: 2025/5/21 11:03
# @Author: windyzhao
import uuid

import pandas as pd
import datetime
from typing import List, Dict, Any

from django.db import transaction
from django.utils import timezone

from apps.alerts.common.alert_engine import RuleEngine
from apps.alerts.common.alert_rules import VALID_RULES, format_alert_message
from apps.alerts.constants import EventLevel
from apps.alerts.models import Event, Alert


class AlertProcessor:
    def __init__(self, rules_config: Dict[str, Any] = None, window_size: str = "10min"):
        self.rules_config = rules_config or VALID_RULES.dict()
        self.window_size = window_size
        self.engine = self._init_engine()
        self.event_fields = [
            "event_id", "external_id", "item", "received_at", "status", "level", "source__name",
            "source_id", "title", "description", "resource_id", "resource_type", "resource_name", "value"
        ]
        self.now = timezone.now()

    def _init_engine(self) -> RuleEngine:
        """初始化规则引擎"""
        engine = RuleEngine(
            window_size=self.window_size,
        )
        for rule in self.rules_config['rules']:
            engine.add_rule(rule)
        return engine

    def get_events(self) -> pd.DataFrame:
        """获取事件数据"""
        get_time = int(self.window_size.split("min")[0])
        start_time = self.now - datetime.timedelta(minutes=get_time)
        instances = Event.objects.filter(
            received_at__gte=start_time,
            received_at__lt=self.now,
            source__is_active=True,
        ).values(*self.event_fields)
        return pd.DataFrame(list(instances))

    def process(self) -> List[Dict[str, Any]]:
        """处理主流程"""
        format_alert_list = []
        try:
            # 1. 获取事件数据
            events = self.get_events()
            # 2. 执行规则检测
            alerts = self.engine.process_events(events)
            # 3. 生成告警
            for rule_name, result in alerts.items():
                if result['triggered']:
                    # 根据event_id拿出evnet的原始数据
                    for source_name, _event_dict in result['alert_sources'].items():
                        event_ids = _event_dict['event_ids']  # 事件ID列表[[], [], []]
                        for event_id_list in event_ids:
                            event_data = events[events['event_id'].isin(event_id_list)].to_dict('records')
                            # 生成告警
                            alert = {
                                "rule_name": rule_name,
                                "description": result['description'],
                                "severity": result['severity'],
                                "event_data": event_data,
                                "event_ids": event_id_list,
                                "created_at": self.now,
                                "rule": result["rule"],
                                "source_name": source_name
                            }
                            # 保存告警数据
                            format_alert = self.format_event_to_alert(alert)
                            format_alert_list.append(format_alert)

            return format_alert_list
        except Exception as e:
            print(f"Processing failed: {str(e)}")
            return []

    @staticmethod
    def bulk_create_alerts(alerts: List[Dict[str, Any]]) -> None:
        """批量创建告警 - 高性能原生SQL版"""
        if not alerts:
            return

        with transaction.atomic():
            alert_ids = []
            # 1. 批量插入告警
            for alert in alerts:
                events = alert.pop("events")

                # 插入告警
                alert_obj = Alert(**alert)
                alert_obj.save()
                alert_id = alert_obj.id
                alert_ids.append(alert_id)

                # 2. 批量插入告警-事件关系
                through_model = Alert.events.through
                through_values = [
                    through_model(alert_id=alert_id, event_id=event.id)
                    for event in events
                ]
                through_model.objects.bulk_create(through_values)

    def format_event_to_alert(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """格式化事件数据为告警数据"""
        events = params["event_data"]
        event_ids = params["event_ids"]
        rule = params["rule"]
        source_name = params["source_name"]
        _instances, level = self.get_event_instances(event_ids=event_ids)
        base_event = events[0]  # 取第一个事件作为基础事件
        title, content = format_alert_message(rule=rule, event_data=base_event)
        alert = {
            "alert_id": f"ALERT-{uuid.uuid4().hex.upper()}",
            "level": level,  # 告警级别 event里最高的level
            "title": title,
            "content": content,
            "item": base_event["item"],
            "resource_id": base_event["resource_id"],
            "resource_name": base_event["resource_name"],
            "resource_type": base_event["resource_type"],
            "first_event_time": _instances.first().received_at,
            "last_event_time": _instances.last().received_at,
            # event id
            "events": _instances,
            "source_name": source_name,  # 告警源名称
        }

        return alert

    @staticmethod
    def get_event_instances(event_ids: List[str]):
        """根据事件ID获取事件实例"""

        instances = Event.objects.filter(event_id__in=event_ids)

        # 定义级别优先级映射（数字越大优先级越高）
        level_priority = {
            EventLevel.FATAL: 4,
            EventLevel.SEVERITY: 3,
            EventLevel.WARNING: 2,
            EventLevel.REMAIN: 1
        }

        # 获取所有事件的级别
        event_levels = set(instances.values_list('level', flat=True))

        # 根据优先级排序找出最高级别
        highest_level = max(event_levels, key=lambda level: level_priority.get(level, 0))

        return instances, highest_level

    def main(self):
        alart_list = self.process()
        self.bulk_create_alerts(alerts=alart_list)
