# -- coding: utf-8 --
from django.core.management.base import BaseCommand
from apps.alerts.common.aggregation.alert_processor import AlertProcessor


class Command(BaseCommand):
    help = 'Process alerts using rule engine with different window types based on correlation rules'

    def add_arguments(self, parser):
        parser.add_argument(
            '--correlation_rule_id',
            type=int,
            help='Specific correlation rule ID to process (optional)'
        )
        
        # 保留向后兼容的参数
        parser.add_argument(
            '--window_size',
            type=str,
            default='10min',
            help='Default window size for compatibility (deprecated, use correlation rules instead)'
        )
        
        parser.add_argument(
            '--window_type',
            type=str,
            default='sliding',
            choices=['sliding', 'fixed', 'session'],
            help='Default window type for compatibility (deprecated, use correlation rules instead)'
        )

    def handle(self, *args, **options):
        correlation_rule_id = options.get('correlation_rule_id')
        
        if correlation_rule_id:
            # 处理特定的关联规则
            self._process_specific_correlation_rule(correlation_rule_id)
        else:
            # 处理所有激活的关联规则
            self._process_all_correlation_rules()

    def _process_specific_correlation_rule(self, correlation_rule_id: int):
        """处理特定的关联规则"""
        try:
            from apps.alerts.models import CorrelationRules
            from apps.alerts.common.aggregation.alert_processor import AlertProcessor
            
            correlation_rule = CorrelationRules.objects.get(
                id=correlation_rule_id,
                aggregation_rules__is_active=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'开始处理关联规则: {correlation_rule.name} - '
                    f'窗口类型: {correlation_rule.window_type}, '
                    f'窗口大小: {correlation_rule.window_size}'
                )
            )

            processor = AlertProcessor(
                window_size=correlation_rule.window_size, 
                window_type=correlation_rule.window_type
            )
            processor.main()

            self.stdout.write(
                self.style.SUCCESS(f'关联规则处理完成: {correlation_rule.name}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'关联规则处理失败: {str(e)}')
            )
            raise

    def _process_all_correlation_rules(self):
        """处理所有激活的关联规则"""
        try:
            from apps.alerts.models import CorrelationRules
            from apps.alerts.common.aggregation.alert_processor import AlertProcessor
            
            # 获取所有激活的关联规则
            correlation_rules = CorrelationRules.objects.filter(
                aggregation_rules__is_active=True
            ).distinct()
            
            if not correlation_rules.exists():
                self.stdout.write(
                    self.style.WARNING('没有找到激活的关联规则，使用默认配置')
                )
                # 使用默认配置
                processor = AlertProcessor()
                processor.main()
                return

            self.stdout.write(
                self.style.SUCCESS(f'开始处理 {len(correlation_rules)} 个关联规则')
            )

            # 使用多窗口类型处理器
            processor = AlertProcessor()
            processor.main()

            self.stdout.write(
                self.style.SUCCESS('所有关联规则处理完成')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'告警处理失败: {str(e)}')
            )
            raise
