from django.core.management import BaseCommand

from apps.core.logger import monitor_logger as logger
from apps.log.plugins.plugin_migrate import migrate_collector, migrate_collect_type


class Command(BaseCommand):
    help = "日志插件初始化命令"

    def handle(self, *args, **options):
        logger.info("初始化日志插件开始！")
        migrate_collector()
        migrate_collect_type()
        logger.info("日志插件初始化完成！")
