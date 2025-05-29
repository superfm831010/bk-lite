import logging

from django.core.management import BaseCommand

from apps.monitor.tasks import sync_instance_and_group

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "监控实例自动发现"

    def handle(self, *args, **options):
        logger.info("监控实例自动发现开始！")
        sync_instance_and_group()
        logger.info("监控实例自动发现完成！")
