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
        from apps.alerts.service.init_alert_sources import init_builtin_alert_sources
        init_builtin_alert_sources()
    except Exception as e:
        logger.error(f"Failed to initialize built-in alert sources: {e}")
        pass

    # 初始化告警级别
    init_levels(**kwargs)


def adapters(**kwargs):
    """注册告警源适配器"""
    try:
        from apps.alerts.common.source_adapter.base import AlertSourceAdapterFactory
        from apps.alerts.common.source_adapter.restful import RestFulAdapter
        AlertSourceAdapterFactory.register_adapter('restful', RestFulAdapter)
    except Exception as e:
        logger.error(f"Failed to register alert source adapter: {e}")
        pass


def init_levels(**kwargs):
    """初始化告警级别"""
    logger.info("===Start Initializing Alert Levels==")
    try:
        from apps.alerts.constants import DEFAULT_LEVEL
        level_model = kwargs["sender"].models["level"]
        for level_data in DEFAULT_LEVEL:
            level_data["built_in"] = True
            level_model.objects.get_or_create(level_type=level_data["level_type"], level_id=level_data["level_id"],
                                              level_name=level_data["level_name"],
                                              defaults=level_data)
    except Exception as e:
        logger.error(f"Failed to initialize alert levels: {e}")
        pass

    logger.info("===Alert Levels Initialization Completed===")
