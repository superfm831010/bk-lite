from django.db import transaction

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.monitor.models import MonitorObjectOrganizationRule, MonitorInstanceOrganization
from apps.monitor.tasks.grouping_rule import RuleGrouping

class OrganizationRule:

    @staticmethod
    def del_organization_rule(rule_id: int, del_instance_org: bool):
        """根据规则删除实例组织"""

        with transaction.atomic():
            # 检查规则是否存在
            rule = MonitorObjectOrganizationRule.objects.select_related("monitor_object").filter(id=rule_id).first()
            if not rule:
                raise BaseAppException(f"规则 ID {rule_id} 不存在")

            # 删除关联的监控实例组织
            if del_instance_org:
                asso_list = RuleGrouping.get_asso_by_condition_rule(rule)
                MonitorInstanceOrganization.objects.filter(
                    monitor_instance_id__in=[asso[0] for asso in asso_list],
                    organization__in=rule.organizations
                ).delete()

            # 删除规则
            rule.delete()
