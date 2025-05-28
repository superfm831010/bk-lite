# -- coding: utf-8 --
# @File: init_alert_sources.py
# @Time: 2025/5/14 16:39
# @Author: windyzhao

from django.db import transaction

from apps.alerts.common.source_adapter.constants import DEFAULT_SOURCE_CONFIG
from apps.alerts.models import AlertSource
from apps.alerts.constants import AlertsSourceTypes, AlertAccessType

# 内置告警源配置
BUILTIN_ALERT_SOURCES = [
    # {
    #     "name": "Prometheus",
    #     "source_id": "prometheus",
    #     "source_type": AlertsSourceTypes.PROMETHEUS,
    #     "config": {
    #         "base_url": "",
    #         "api_path": "/api/v1/alerts",
    #         "timeout": 10,
    #         "verify_ssl": True,
    #     },
    #     "access_type": AlertAccessType.BUILT_IN,
    #     "is_active": True,
    #     "is_effective": True,
    #     "description": "内置Prometheus告警源",
    # },
    # {
    #     "name": "Webhook",
    #     "source_id": "webhook",
    #     "source_type": AlertsSourceTypes.WEBHOOK,
    #     "config": {},
    #     "access_type": AlertAccessType.BUILT_IN,
    #     "is_active": True,
    #     "is_effective": True,
    #     "description": "内置Webhook告警源",
    # },
    {
        "name": "x-monitor",
        "source_id": "monitor",
        "source_type": AlertsSourceTypes.MONITOR,
        "config": DEFAULT_SOURCE_CONFIG,
        "access_type": AlertAccessType.BUILT_IN,
        "is_active": True,
        "is_effective": True,
        "description": "内置x-monitor告警源",
    },
]


def init_builtin_alert_sources():
    """初始化内置告警源"""
    with transaction.atomic():
        for src in BUILTIN_ALERT_SOURCES:
            AlertSource.all_objects.get_or_create(
                source_id=src["source_id"],
                defaults=src
            )
