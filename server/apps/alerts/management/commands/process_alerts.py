# -- coding: utf-8 --
from django.core.management.base import BaseCommand
from apps.alerts.common.aggregation.alert_processor import AlertProcessor


class Command(BaseCommand):
    help = 'Process alerts using rule engine'

    def add_arguments(self, parser):
        parser.add_argument(
            '--window_size',
            type=str,
            default='default',
            help='Window size for alert processing (e.g., 10min, 1h, etc.) example: 10min'
        )

    def handle(self, *args, **options):
        window_size = options.get('window_size', '10min')

        # 使用新的规则管理器
        processor = AlertProcessor(window_size=window_size)
        processor.main()

        self.stdout.write(self.style.SUCCESS('Successfully processed alerts'))
