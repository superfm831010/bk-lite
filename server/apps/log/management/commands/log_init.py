from django.core.management import BaseCommand

from apps.core.logger import log_logger as logger
from apps.log.plugins.plugin_migrate import migrate_collector, migrate_collect_type


def init_stream():
    from apps.log.models import Stream
    if not Stream.objects.filter(id='default').exists():
        Stream.objects.create(id='default', name='Default', created_by="system", updated_by="system")


class Command(BaseCommand):
    help = "日志插件初始化命令"

    def handle(self, *args, **options):
        logger.info("初始化日志插件开始！")
        migrate_collector()
        migrate_collect_type()
        logger.info("日志插件初始化完成！")

        logger.info("初始化默认数据流开始！")
        init_stream()
        logger.info("默认数据流初始化完成！")