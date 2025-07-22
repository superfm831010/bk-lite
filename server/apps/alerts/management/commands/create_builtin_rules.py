from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from apps.alerts.models import AggregationRules
from apps.alerts.utils.util import image_to_base64
from apps.core.logger import alert_logger as logger

INIT_RULES = [
    {
        'rule_id': 'high_level_event_aggregation',
        'name': 'High Level Event Aggregation',
        'description': {
            "en": "Rule definition: \n1. Filtering method: event level higher than \"warning\"\n2. Aggregation dimension: Object instances of events\n3. Aggregation strategy: Aggregate based on the same object instance of the event, with the alert level being the lowest level of the event.\nCommonly used in scenarios where performance evaluation of a single operational object requires a combination of multiple dimensions for analysis, such as abnormal server performance, abnormal database performance, etc",
            "zh": "规则定义： \n1，过滤方式：event等级高于“warning”\n2，汇聚维度：event的对象实例\n3，聚合策略：按照event相同对象实例进行聚合，alert等级为event的最低等级。\n常用于单种运维对象的性能判断需要多个维度结合分析的场景，例如：服务器的性能异常、数据库的性能异常等"
        },
        'template_title': '',
        'template_content': '',
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
                'aggregation_key': ['resource_type', 'resource_name']
            }
        ]
    },
    {
        'rule_id': 'critical_event_aggregation',
        'name': 'Critical Event Aggregation',
        'description': {
            "en": "Rule definition:\nRule definition: 1. Filtering method: event type\n2. Aggregation strategy: Every minute, when a certain event is abnormal, it will aggregate the repeated events of this object within 1 minute and immediately generate an alert.Commonly used scenarios for website testing",
            "zh": "规则定义：\n1，过滤方式：event类型\n2，聚合策略：每隔1分钟，检测当某个事件异常时，将1分钟内这个对象重复的事件聚合，立刻产生alert。常用于网站拨测的场景"
        },
        'template_title': '',
        'template_content': '',
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
                'aggregation_key': ['resource_type', 'resource_name']
            }
        ]
    },
    {
        'rule_id': 'error_scenario_handling',
        'name': 'Error Scenario Handling',
        'description': {
            "zh": "当某个操作失败时，如果10分钟内没有继续修正的动作，则意味着构建失败，发出告警。如果10分钟内依旧持续操作但是依旧失败，意味着有人在介入，此时持续等待不发出告警。如果10分钟内收到操作成功的事件，则关闭等待，不发出告警。\n 常用于比如流水线构建场景，如果某流水线构建失败后，10分钟内没有继续操作的事件，则意味着短时间内代码问题无法解决，发出告警",
            "en": "When an operation fails and there are no further corrective actions within 10 minutes, it means that the build has failed and an alarm is raised. If the operation continues for 10 minutes but still fails, it means that someone is intervening and waiting continuously without issuing an alarm. If a successful operation event is received within 10 minutes, turn off waiting and no alarm will be issued.\n Commonly used in scenarios such as pipeline construction, if there is no event to continue operating within 10 minutes after a pipeline construction failure, it means that the code problem cannot be solved in a short period of time and an alarm is issued",
        },
        'template_title': '',
        'template_content': '',
        'severity': "warning",
        'is_active': True,
        'condition': [
            {
                'type': 'filter_and_check',
                'filter': {
                    'resource_type': 'jenkins',
                },
                'target_field': 'item',
                'target_field_value': 'jenkins_build_status',
                'target_value_field': 'value',
                'target_value': 0,
                'operator': '==',
                'aggregation_key': ['resource_type', 'resource_name'],
                # 新增：成功事件关闭会话的条件
                'session_close': {
                    'type': 'session_close_condition',
                    'filter': {
                        'resource_type': 'jenkins',
                    },
                    'target_field': 'item',
                    'target_field_value': 'jenkins_build_status',
                    'target_value_field': 'value',
                    'target_value': 1,  # 成功状态
                    'operator': '==',
                    'action': 'close_session',  # 关闭会话动作
                    'aggregation_key': ['resource_type', 'resource_name']
                }
            }
        ]

    }
]


class Command(BaseCommand):
    help = '创建内置告警聚合规则'
    base_path = "/apps/alerts/images"

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
                        image = self.get_rule_image(rule_data['rule_id'])
                        if image:
                            setattr(existing_rule, "image", image)
                        else:
                            logger.warning(f"未找到规则图片: {rule_data['rule_id']}")
                        existing_rule.save()
                        updated_count += 1
                        logger.info(f"更新聚合规则: {rule_data['name']}")
                    else:
                        logger.info(f"规则已存在，跳过: {rule_data['name']}")
                        continue
                else:
                    image = self.get_rule_image(rule_data['rule_id'])
                    if image:
                        rule_data['image'] = image
                    else:
                        logger.warning(f"未找到规则图片: {rule_data['rule_id']}")
                    # 创建新规则
                    AggregationRules.objects.create(**rule_data)
                    created_count += 1
                    logger.info(f"创建聚合规则: {rule_data['name']}")

            except Exception as e:
                logger.error(f"处理规则失败 {rule_data.get('name', 'Unknown')}: {str(e)}")

        logger.info(f"聚合规则处理完成 - 创建: {created_count}, 更新: {updated_count}")
        return created_count, updated_count

    def get_rule_image(self, rule_id):
        image_path = f"{settings.BASE_DIR}/{self.base_path}/{rule_id}.png"
        try:
            base64_data = image_to_base64(image_path=image_path, output_format="png")
        except Exception as e:
            logger.error(f"获取规则图片失败 {rule_id}: {str(e)}")
            return
        return base64_data
