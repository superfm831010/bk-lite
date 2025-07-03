from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.logger import alert_logger as logger


class Command(BaseCommand):
    help = "初始化内置告警源"

    def handle(self, *args, **options):
        """初始化内置告警源"""
        logger.info("===开始初始化内置告警源===")

        try:
            from apps.alerts.service.init_alert_sources import BUILTIN_ALERT_SOURCES
            from apps.alerts.models import AlertSource
            with transaction.atomic():
                for src in BUILTIN_ALERT_SOURCES:
                    AlertSource.all_objects.get_or_create(
                        source_id=src["source_id"],
                        defaults=src
                    )
            self.stdout.write(
                self.style.SUCCESS('成功初始化内置告警源')
            )
            logger.info("===内置告警源初始化完成===")

        except Exception as e:
            error_msg = f"初始化内置告警源失败: {e}"
            logger.error(error_msg)
            self.stdout.write(self.style.ERROR(error_msg))
            raise
