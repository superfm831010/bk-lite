# -- coding: utf-8 --
# @File: base.py
# @Time: 2025/5/13 15:48
# @Author: windyzhao
import datetime
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from django.utils import timezone

from apps.alerts.models import AlertSource, Event
from apps.alerts.common.source_adapter import logger
from apps.alerts.utils.util import split_list


class AuthenticationSourceError(Exception):
    """自定义认证异常"""

    def __init__(self, msg):
        self.message = msg


class AlertSourceAdapter(ABC):
    """告警源适配器基类"""

    def __init__(self, alert_source: AlertSource, secret: str = None, events: List = []):
        self.alert_source = alert_source
        self.config = alert_source.config
        self.secret = secret
        self.alerts = events
        self.mapping = self.alert_source.config.get("event_fields_mapping", {})

    @abstractmethod
    def authenticate(self, *args, **kwargs) -> bool:
        """认证告警源"""
        pass

    @abstractmethod
    def fetch_alerts(self) -> List[Dict[str, Any]]:
        """从告警源获取告警数据"""
        pass

    def mapping_fields_to_event(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """将告警字段映射到事件字段"""
        result = {}
        for key, field in self.mapping.items():
            _value = alert.get(field, None)
            if _value is None:
                continue
            if key == "start_time" or key == "end_time":
                _value = self.timestamp_to_datetime(_value)

            if key == "value":
                _value = float(_value) if _value and isinstance(_value, str) and _value.isdigit() else _value

            result[key] = _value

        return result

    def create_events(self, alerts):
        """将原始告警数据转换为Event对象"""
        events = []
        for alert in alerts:
            try:
                event = self._transform_alert_to_event(alert)
                self.add_base_fields(event, alert)
                events.append(event)
            except Exception as e:
                logger.error(f"Failed to transform alert: {alert}, error: {e}")
        self.bulk_save_events(events)

    def add_base_fields(self, event: Event, alert: Dict[str, Any]):
        """添加基础字段"""
        event.source = self.alert_source
        event.raw_data = alert
        event.event_id = f"EVENT-{uuid.uuid4().hex}"

    @staticmethod
    def bulk_save_events(events: List[Event]):
        """批量保存事件"""
        if events:
            bulk_create_events = split_list(events, 100)
            for event_batch in bulk_create_events:
                Event.objects.bulk_create(event_batch, ignore_conflicts=True)  # 跳过唯一性约束
            logger.info(f"Bulk saved {len(events)} events.")

    def _transform_alert_to_event(self, alert: Dict[str, Any]) -> Event:
        """将单个告警数据转换为Event对象"""
        data = self.mapping_fields_to_event(alert)
        event = Event(**data)
        return event

    @staticmethod
    def timestamp_to_datetime(timestamp: str) -> datetime:
        """将时间戳转换为datetime对象"""
        # 先转为 naive datetime timestamp 微妙
        dt = datetime.datetime.fromtimestamp(int(timestamp) / 1000 if len(timestamp) == 13 else int(timestamp))
        # 转为 aware datetime（带时区）
        return timezone.make_aware(dt, timezone.get_current_timezone())

    def main(self, alerts=None):
        """使适配器实例可调用"""
        if not alerts:
            alerts = self.alerts
        self.create_events(alerts)


class AlertSourceAdapterFactory:
    """告警源适配器工厂"""

    _adapters = {}

    @classmethod
    def register_adapter(cls, source_type: str, adapter_class):
        """注册适配器"""
        cls._adapters[source_type] = adapter_class

    @classmethod
    def get_adapter(cls, alert_source: AlertSource):
        """获取适配器实例"""
        adapter_class = cls._adapters.get(alert_source.source_type)
        if not adapter_class:
            raise ValueError(f"No adapter found for source type: {alert_source.source_type}")
        return adapter_class

    @classmethod
    def get_supported_types(cls) -> List[str]:
        """获取支持的告警源类型"""
        return list(cls._adapters.keys())
