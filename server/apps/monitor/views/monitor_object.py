from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.utils.permission_utils import get_permissions_rules, check_instance_permission
from apps.core.utils.web_utils import WebUtils
from apps.monitor.constants import INSTANCE_MODULE, POLICY_MODULE
from apps.monitor.filters.monitor_object import MonitorObjectFilter
from apps.monitor.language.service import SettingLanguage
from apps.monitor.models import MonitorInstance, MonitorPolicy
from apps.monitor.models.monitor_object import MonitorObject
from apps.monitor.serializers.monitor_object import MonitorObjectSerializer
from apps.monitor.services.monitor_object import MonitorObjectService
from config.drf.pagination import CustomPageNumberPagination


class MonitorObjectVieSet(viewsets.ModelViewSet):
    queryset = MonitorObject.objects.all()
    serializer_class = MonitorObjectSerializer
    filterset_class = MonitorObjectFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="monitor_object_list",
        operation_description="监控对象列表",
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        results = serializer.data
        lan = SettingLanguage(request.user.locale)
        for result in results:
            result["display_type"] = lan.get_val("MONITOR_OBJECT_TYPE", result["type"]) or result["type"]
            result["display_name"] = lan.get_val("MONITOR_OBJECT", result["name"]) or result["name"]

        if request.GET.get("add_instance_count") in ["true", "True"]:

            inst_res = get_permissions_rules(
                request.user,
                request.COOKIES.get("current_team"),
                "monitor",
                f"{INSTANCE_MODULE}",
            )

            instance_permissions, cur_team = inst_res.get("data", {}), inst_res.get("team", [])

            inst_objs = MonitorInstance.objects.filter(is_deleted=False).prefetch_related("monitorinstanceorganization_set")
            inst_map = {}
            for inst_obj in inst_objs:
                monitor_object_id = inst_obj.monitor_object_id
                instance_id = inst_obj.id
                teams = {i.organization for i in inst_obj.monitorinstanceorganization_set.all()}
                _check = check_instance_permission(monitor_object_id, instance_id, teams, instance_permissions, cur_team)
                if not _check:
                    continue
                if monitor_object_id not in inst_map:
                    inst_map[monitor_object_id] = 0
                inst_map[monitor_object_id] += 1

            for result in results:
                result["instance_count"] = inst_map.get(result["id"], 0)

        if request.GET.get("add_policy_count") in ["true", "True"]:
            policy_res = get_permissions_rules(
                request.user,
                request.COOKIES.get("current_team"),
                "monitor",
                f"{POLICY_MODULE}",
            )

            policy_permissions, cur_team = policy_res.get("data", {}), policy_res.get("team", [])

            policy_objs = MonitorPolicy.objects.all().prefetch_related("policyorganization_set")
            policy_map = {}
            for policy_obj in policy_objs:
                monitor_object_id = policy_obj.monitor_object_id
                instance_id = policy_obj.id
                teams = {i.organization for i in policy_obj.policyorganization_set.all()}
                _check = check_instance_permission(monitor_object_id, instance_id, teams, policy_permissions, cur_team)
                if not _check:
                    continue
                if monitor_object_id not in policy_map:
                    policy_map[monitor_object_id] = 0
                policy_map[monitor_object_id] += 1

            for result in results:
                result["policy_count"] = policy_map.get(result["id"], 0)

        # 排序
        sorted_results = MonitorObjectService.sort_items(results)

        return WebUtils.response_success(sorted_results)

    @swagger_auto_schema(
        operation_id="monitor_object_create",
        operation_description="创建监控对象",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_update",
        operation_description="更新监控对象",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_partial_update",
        operation_description="部分更新监控对象",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_retrieve",
        operation_description="查询监控对象",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_del",
        operation_description="删除监控对象",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_order",
        operation_description="监控对象排序",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "type": openapi.Schema(type=openapi.TYPE_STRING, description="对象类型"),
                    "name_list": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="对象名称列表"),
                }
            )
        )
    )
    @action(methods=['post'], detail=False, url_path='order')
    def order(self, request):
        MonitorObjectService.set_object_order(request.data)
        return WebUtils.response_success()
