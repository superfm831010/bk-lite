from django.core.management.base import BaseCommand
from apps.alerts.common.rules.rule_manager import get_rule_manager
from apps.alerts.common.aggregation.alert_processor import AlertProcessor
import json


class Command(BaseCommand):
    help = 'Manage alert rules'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['list', 'add', 'update', 'remove', 'stats', 'process'],
            help='Action to perform'
        )
        parser.add_argument('--rule-name', type=str, help='Rule name')
        parser.add_argument('--rule-config', type=str, help='Rule configuration JSON')

    def handle(self, *args, **options):
        rule_manager = get_rule_manager()
        action = options.get('action')

        if action == 'list':
            self.list_rules(rule_manager)
        elif action == 'add':
            self.add_rule(rule_manager, options)
        elif action == 'update':
            self.update_rule(rule_manager, options)
        elif action == 'remove':
            self.remove_rule(rule_manager, options)
        elif action == 'stats':
            self.show_statistics(rule_manager)
        elif action == 'process':
            self.process_events()

    def list_rules(self, rule_manager):
        """列出所有规则"""
        rules = rule_manager.get_active_rules()
        self.stdout.write(f"Active rules ({len(rules)}):")
        for rule in rules:
            self.stdout.write(f"  - {rule.name}: {rule.description}")

    def add_rule(self, rule_manager, options):
        """添加规则"""
        rule_config = options.get('rule_config')
        if not rule_config:
            self.stdout.write(self.style.ERROR('Rule config is required'))
            return

        try:
            config = json.loads(rule_config)
            if rule_manager.add_rule(config):
                self.stdout.write(self.style.SUCCESS(f'Rule added successfully'))
            else:
                self.stdout.write(self.style.ERROR('Failed to add rule'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON config'))

    def update_rule(self, rule_manager, options):
        """更新规则"""
        rule_name = options.get('rule_name')
        rule_config = options.get('rule_config')
        
        if not rule_name or not rule_config:
            self.stdout.write(self.style.ERROR('Rule name and config are required'))
            return

        try:
            config = json.loads(rule_config)
            if rule_manager.update_rule(rule_name, config):
                self.stdout.write(self.style.SUCCESS(f'Rule {rule_name} updated successfully'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to update rule {rule_name}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON config'))

    def remove_rule(self, rule_manager, options):
        """删除规则"""
        rule_name = options.get('rule_name')
        if not rule_name:
            self.stdout.write(self.style.ERROR('Rule name is required'))
            return

        if rule_manager.remove_rule(rule_name):
            self.stdout.write(self.style.SUCCESS(f'Rule {rule_name} removed successfully'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to remove rule {rule_name}'))

    def show_statistics(self, rule_manager):
        """显示统计信息"""
        stats = rule_manager.get_rule_statistics()
        self.stdout.write("Rule Statistics:")
        self.stdout.write(f"  Total rules: {stats['total_rules']}")
        self.stdout.write(f"  Active rules: {stats['active_rules']}")
        self.stdout.write(f"  Inactive rules: {stats['inactive_rules']}")
        
        self.stdout.write("  Rule types:")
        for rule_type, count in stats['rule_types'].items():
            self.stdout.write(f"    {rule_type}: {count}")
        
        self.stdout.write("  Severity distribution:")
        for severity, count in stats['severity_distribution'].items():
            self.stdout.write(f"    {severity}: {count}")

    def process_events(self):
        """处理事件"""
        processor = AlertProcessor()
        format_alerts, update_alerts = processor.process()
        
        self.stdout.write(f"Processed events:")
        self.stdout.write(f"  New alerts: {len(format_alerts)}")
        self.stdout.write(f"  Updated alerts: {len(update_alerts)}")
