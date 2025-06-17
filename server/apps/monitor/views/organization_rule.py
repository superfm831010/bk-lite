from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.core.utils.web_utils import WebUtils
from apps.monitor.filters.monitor_object import MonitorObjectOrganizationRuleFilter
from apps.monitor.models import MonitorObjectOrganizationRule
from apps.monitor.serializers.monitor_object import MonitorObjectOrganizationRuleSerializer
from apps.monitor.services.organization_rule import OrganizationRule
from config.drf.pagination import CustomPageNumberPagination


class MonitorObjectOrganizationRuleVieSet(viewsets.ModelViewSet):
    queryset = MonitorObjectOrganizationRule.objects.all()
    serializer_class = MonitorObjectOrganizationRuleSerializer
    filterset_class = MonitorObjectOrganizationRuleFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_list",
        operation_description="监控实例分组规则列表",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_create",
        operation_description="创建监控实例分组规则",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_update",
        operation_description="更新监控实例分组规则",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_partial_update",
        operation_description="部分更新监控实例分组规则",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_retrieve",
        operation_description="查询监控实例分组规则",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_del",
        operation_description="删除监控实例分组规则",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="分组规则ID",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'del_instance_org',
                openapi.IN_QUERY,
                description="是否删除实例组织",
                type=openapi.TYPE_BOOLEAN,
                required=False,
                default=False
            )
        ],
    )
    def destroy(self, request, *args, **kwargs):
        del_instance_org = request.query_params.get('del_instance_org', "false").lower() in ['true', '1', 'yes']
        OrganizationRule.del_organization_rule(rule_id=kwargs.get('pk'), del_instance_org=del_instance_org)
        return WebUtils.response_success()
