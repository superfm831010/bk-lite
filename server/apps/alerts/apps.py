# -- coding: utf-8 --
# @File: apps.py
# @Time: 2025/5/9 14:51
# @Author: windyzhao
from django.apps import AppConfig
from django.db.models.signals import post_migrate

from apps.core.logger import logger


class AlertsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.alerts"

    def ready(self):
        # 注册告警源适配器
        adapters()
        post_migrate.connect(app_init, sender=self)


def app_init(**kwargs):
    """应用初始化"""

    # 初始化内置告警源
    try:
        from apps.alerts.common.init_alert_sources import init_builtin_alert_sources
        init_builtin_alert_sources()
    except Exception as e:
        logger.error(f"Failed to initialize built-in alert sources: {e}")
        pass


def adapters(**kwargs):
    """注册告警源适配器"""
    try:
        from apps.alerts.common.source_adapter.base import AlertSourceAdapterFactory
        from apps.alerts.common.source_adapter.monitor import MonitorAdapter
        AlertSourceAdapterFactory.register_adapter('monitor', MonitorAdapter)
    except Exception as e:
        logger.error(f"Failed to register alert source adapter: {e}")
        pass
