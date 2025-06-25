from django.core.management.base import BaseCommand
from django.db import transaction

from apps.alerts.models import AggregationRules
from apps.core.logger import alert_logger as logger

INIT_RULES = [
    {
        'rule_id': 'high_cpu',
        'name': 'CPU High Usage',
        'description': 'CPU使用率超过85%',
        'template_title': '【${resource_type}】${resource_name} CPU使用率过高',
        'template_content': 'CPU使用率: ${value}%\n阈值: 85%\n持续时间: ${duration}分钟',
        'severity': 'warning',  # warning
        'is_active': False,
        'condition': [
            {
                'type': 'threshold',
                'field': 'cpu_usage',
                'threshold': 85.0,
                'operator': '>='
            }
        ]
    },
    {
        'rule_id': 'sustained_high_cpu',
        'name': 'CPU Sustained High Usage',
        'description': 'CPU连续3个周期使用率超过80%',
        'template_title': '【${resource_type}】${resource_name} CPU持续高使用率',
        'template_content': 'CPU使用率: ${value}%\n阈值: 80%\n连续周期: 3',
        'severity': 'warning',  # warning
        'is_active': False,
        'condition': [
            {
                'type': 'sustained',
                'field': 'cpu_usage',
                'threshold': 80.0,
                'operator': '>=',
                'required_consecutive': 3
            }
        ]
    },
    {
        'rule_id': 'disk_io_latency_spike',
        'name': 'Disk IO Latency Spike',
        'description': '磁盘IO延迟大于5.0',
        'template_title': '【${resource_type}】${resource_name} 磁盘IO延迟异常',
        'template_content': '磁盘IO延迟: ${value}ms\n阈值: 5.0ms',
        'severity': 'warning',  # severity
        'is_active': False,
        'condition': [
            {
                'type': 'threshold',
                'field': 'disk_io_latency',
                'threshold': 5.0,
                'operator': '>'
            }
        ]
    },
    {
        'rule_id': 'cpu_trend_spike',
        'name': 'CPU Trend Spike',
        'description': 'CPU使用率突增超过20%',
        'template_title': '【${resource_type}】${resource_name} CPU使用率突增',
        'template_content': 'CPU使用率突增: ${value}%\n基线: ${baseline}%\n阈值: 20%',
        'severity': 'warning',  # fatal
        'is_active': False,
        'condition': [
            {
                'type': 'trend',
                'field': 'cpu_usage',
                'threshold': 20.0,
                'operator': '>',
                'baseline_window': 5,
                'trend_method': 'percentage'
            }
        ]
    },
    {
        'rule_id': 'prev_status_equals',
        'name': 'Status Recovery Detection',
        'description': '状态恢复检测规则',
        'template_title': '【${resource_type}】${resource_name} 状态变更',
        'template_content': '资源状态从 ${prev_status} 变更为 ${status}',
        'severity': 'warning',  # fatal
        'is_active': False,
        'condition': [
            {
                'type': 'prev_field_equals',
                'field': '',
                'group_by': ['source_id', 'resource_type', 'resource_id', 'item'],
                'prev_status_field': 'status',
                'prev_status_value': 'closed'
            }
        ]
    },
    {
        'rule_id': 'jenkins_single_failure',
        'name': 'Jenkins Single Build Failure',
        'description': 'Jenkins单次构建失败',
        'template_title': 'Jenkins构建失败 - ${resource_name}',
        'template_content': '流水线: ${resource_name}\n状态: 构建失败\n构建号: ${value}\n错误信息: ${description}',
        'severity': "warning",  # warning
        'is_active': False,
        'condition': [
            {
                'type': 'threshold',
                'field': 'build_status',
                'threshold': 0.0,
                'operator': '=='
            }
        ]
    },
    {
        'rule_id': 'jenkins_sustained_failures',
        'name': 'Jenkins Sustained Build Failures',
        'description': 'Jenkins构建连续失败3次',
        'template_title': 'Jenkins流水线 ${resource_name} 连续构建失败',
        'template_content': '流水线: ${resource_name}\n连续失败次数: 3次',
        'severity': "warning",  # fatal
        'is_active': False,
        'condition': [
            {
                'type': 'sustained',
                'field': 'build_status',
                'threshold': 0.0,
                'operator': '==',
                'required_consecutive': 3,
                'group_by': ['resource_id']
            }
        ]
    },
    {
        'rule_id': 'high_level_event_aggregation',
        'name': 'High Level Event Aggregation',
        'description': '高等级事件聚合规则',
        'template_title': '【${resource_type}】${resource_name} 发生告警',
        'template_content': '资源类型: ${resource_type}\n资源名称: ${resource_name}\n详情: ${description}',
        'severity': "warning",
        'is_active': True,
        'condition': [
            {
                'type': 'level_filter',
                'filter': {},
                'target_field': 'level',
                'target_field_value': 'warning',
                'target_value_field': 'level',
                'target_value': 'warning',
                'operator': '<=',
                'aggregation_key': ['resource_type', 'resource_id', 'resource_name']
            }
        ]
    },
    {
        'rule_id': 'website_monitoring_alert',
        'name': 'Website Monitoring Alert',
        'description': '网站拨测异常告警',
        'template_title': '网站拨测异常 - ${resource_name}',
        'template_content': '网站: ${resource_name}\n拨测状态: 异常\nstatus值: ${value}\n异常详情: ${description}',
        'severity': "warning",
        'is_active': True,
        'condition': [
            {
                'type': 'filter_and_check',
                'filter': {
                    'resource_type': '网站拨测'
                },
                'target_field': 'item',
                'target_field_value': 'status',
                'target_value_field': 'value',
                'target_value': 0,  # 保持为数字类型
                'operator': '==',
                'aggregation_key': ['resource_id']
            }
        ]
    }
]


class Command(BaseCommand):
    help = '创建内置告警聚合规则'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='强制更新已存在的规则',
        )

    def handle(self, *args, **options):
        update = options['update']
        self.stdout.write('开始创建内置告警聚合规则...')

        try:
            with transaction.atomic():
                # 创建聚合规则
                aggregation_rules = self._create_aggregation_rules(force_update=update)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'成功创建 {len(aggregation_rules)} 个聚合规则'
                    )
                )

        except Exception as e:
            logger.error(f"创建内置规则失败: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f'创建规则失败: {str(e)}')
            )

    def _create_aggregation_rules(self, force_update=False):
        """创建或更新聚合规则"""
        created_count = 0
        updated_count = 0

        for rule_data in INIT_RULES:
            try:
                # 查询规则是否存在
                existing_rule = AggregationRules.objects.filter(rule_id=rule_data['rule_id']).first()

                if existing_rule:
                    if force_update:
                        # 更新现有规则
                        for key, value in rule_data.items():
                            if key != 'rule_id':  # rule_id不能修改
                                setattr(existing_rule, key, value)
                        existing_rule.save()
                        updated_count += 1
                        logger.info(f"更新聚合规则: {rule_data['name']}")
                    else:
                        logger.info(f"规则已存在，跳过: {rule_data['name']}")
                        continue
                else:
                    # 创建新规则
                    AggregationRules.objects.create(**rule_data)
                    created_count += 1
                    logger.info(f"创建聚合规则: {rule_data['name']}")

            except Exception as e:
                logger.error(f"处理规则失败 {rule_data.get('name', 'Unknown')}: {str(e)}")

        logger.info(f"聚合规则处理完成 - 创建: {created_count}, 更新: {updated_count}")
        return created_count, updated_count
