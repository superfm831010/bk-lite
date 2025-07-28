from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.core.utils.permission_utils import get_permission_rules, permission_filter
from apps.core.utils.web_utils import WebUtils
from apps.monitor.constants import INSTANCE_MODULE, DEFAULT_PERMISSION
from apps.monitor.models import MonitorInstance, MonitorObject, CollectConfig
from apps.monitor.services.monitor_instance import InstanceSearch
from apps.monitor.services.monitor_object import MonitorObjectService
from apps.rpc.node_mgmt import NodeMgmt


class MonitorInstanceVieSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="获取查询参数枚举",
        manual_parameters=[
            openapi.Parameter("name", openapi.IN_PATH, description="对象名称", type=openapi.TYPE_STRING,
                              required=True),
        ],
    )
    @action(methods=['get'], detail=False, url_path='query_params_enum/(?P<name>[^/.]+)')
    def get_query_params_enum(self, request, name):
        data = InstanceSearch.get_query_params_enum(name)
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_id="monitor_instance_list",
        operation_description="监控实例列表",
        manual_parameters=[
            openapi.Parameter("monitor_object_id", openapi.IN_PATH, description="指标查询参数",
                              type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter("page", openapi.IN_QUERY, description="页码", type=openapi.TYPE_INTEGER),
            openapi.Parameter("page_size", openapi.IN_QUERY, description="每页数据条数", type=openapi.TYPE_INTEGER),
            openapi.Parameter("add_metrics", openapi.IN_QUERY, description="是否添加指标", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter("name", openapi.IN_QUERY, description="监控实例名称", type=openapi.TYPE_STRING),
        ],
    )
    @action(methods=['get'], detail=False, url_path='(?P<monitor_object_id>[^/.]+)/list')
    def monitor_instance_list(self, request, monitor_object_id):
        permission = get_permission_rules(
            request.user,
            request.COOKIES.get("current_team"),
            "monitor",
            f"{INSTANCE_MODULE}.{monitor_object_id}",
        )
        qs = permission_filter(MonitorInstance, permission, team_key="monitorinstanceorganization__organization__in", id_key="id__in")
        page, page_size = request.GET.get("page", 1), request.GET.get("page_size", 10)
        data = MonitorObjectService.get_monitor_instance(
            int(monitor_object_id),
            int(page),
            int(page_size),
            request.GET.get("name"),
            qs,
            bool(request.GET.get("add_metrics", False)),
        )
        # 如果有权限规则，则添加到数据中
        inst_permission_map = {i["id"]: i["permission"] for i in permission.get("instance", [])}
        for instance_info in data["results"]:
            if instance_info["instance_id"] in inst_permission_map:
                instance_info["permission"] = inst_permission_map[instance_info["instance_id"]]
            else:
                instance_info["permission"] = DEFAULT_PERMISSION

        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_id="monitor_instance_search",
        operation_description="监控实例查询",
        manual_parameters=[
            openapi.Parameter("monitor_object_id", openapi.IN_PATH, description="指标查询参数",
                              type=openapi.TYPE_INTEGER, required=True),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "page": openapi.Schema(type=openapi.TYPE_INTEGER, description="页码"),
                "page_size": openapi.Schema(type=openapi.TYPE_INTEGER, description="每页数据条数"),
                "add_metrics": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否添加指标"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="监控实例名称"),
                "vm_params": openapi.Schema(type=openapi.TYPE_OBJECT, description="维度参数"),
            },
        )
    )
    @action(methods=['post'], detail=False, url_path='(?P<monitor_object_id>[^/.]+)/search')
    def monitor_instance_search(self, request, monitor_object_id):

        monitor_obj = MonitorObject.objects.filter(id=monitor_object_id).first()
        if not monitor_obj:
            raise BaseAppException("Monitor object does not exist")

        permission = get_permission_rules(
            request.user,
            request.COOKIES.get("current_team"),
            "monitor",
            f"{INSTANCE_MODULE}.{monitor_object_id}",
        )
        qs = permission_filter(MonitorInstance, permission, team_key="monitorinstanceorganization__organization__in", id_key="id__in")

        search_obj = InstanceSearch(
            monitor_obj,
            dict(**request.data),
            qs=qs,
        )
        data = search_obj.search()
        # 如果有权限规则，则添加到数据中
        inst_permission_map = {i["id"]: i["permission"] for i in permission.get("instance", [])}
        for instance_info in data["results"]:
            if instance_info["instance_id"] in inst_permission_map:
                instance_info["permission"] = inst_permission_map[instance_info["instance_id"]]
            else:
                instance_info["permission"] = DEFAULT_PERMISSION
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_id="generate_monitor_instance_id",
        operation_description="生成监控实例ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "monitor_instance_name": openapi.Schema(type=openapi.TYPE_STRING, description="监控实例名称"),
                "interval": openapi.Schema(type=openapi.TYPE_INTEGER, description="监控实例采集间隔(s)"),
            },
            required=["monitor_instance_name", "interval"]
        )
    )
    @action(methods=['post'], detail=False, url_path='(?P<monitor_object_id>[^/.]+)/generate_instance_id')
    def generate_monitor_instance_id(self, request, monitor_object_id):
        result = MonitorObjectService.generate_monitor_instance_id(
            int(monitor_object_id),
            request.data["monitor_instance_name"],
            request.data["interval"],
        )
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="check_monitor_instance",
        operation_description="校验监控实例是否已存在",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
                properties={
                    "instance_id": openapi.Schema(type=openapi.TYPE_STRING, description="监控实例id"),
                    "instance_name": openapi.Schema(type=openapi.TYPE_INTEGER, description="监控实例名称"),
                },
                required=["instance_id", "instance_name"]
        )
    )
    @action(methods=['post'], detail=False, url_path='(?P<monitor_object_id>[^/.]+)/check_monitor_instance')
    def create_monitor_instance(self, request, monitor_object_id):
        MonitorObjectService.check_monitor_instance(
            int(monitor_object_id),
            request.data
        )
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="autodiscover_monitor_instance",
        operation_description="自动发现监控实例",
    )
    @action(methods=['get'], detail=False, url_path='autodiscover_monitor_instance')
    def autodiscover_monitor_instance(self, request):
        MonitorObjectService.autodiscover_monitor_instance()
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="remove_monitor_instance",
        operation_description="移除监控实例",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "instance_ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="监控实例ID列表"),
                "clean_child_config": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否清除子配置"),
            },
            required=["instance_ids", "clean_child_config"]
        )
    )
    @action(methods=['post'], detail=False, url_path='remove_monitor_instance')
    def remove_monitor_instance(self, request):
        instance_ids = request.data.get("instance_ids", [])
        MonitorInstance.objects.filter(id__in=instance_ids).update(is_deleted=True)
        if request.data.get("clean_child_config"):
            config_objs = CollectConfig.objects.filter(monitor_instance_id__in=instance_ids)
            child_configs, configs = [], []
            for config in config_objs:
                if config.is_child:
                    child_configs.append(config.id)
                else:
                    configs.append(config.id)
            # 删除子配置
            NodeMgmt().delete_child_configs(child_configs)
            # 删除配置
            NodeMgmt().delete_configs(configs)
            # 删除配置对象
            config_objs.delete()
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="monitor_instance_update",
        operation_description="更新监控实例",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "instance_id": openapi.Schema(type=openapi.TYPE_STRING, description="监控实例ID"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="监控实例名称"),
                "organizations": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER, description="组织ID列表")
                ),
            },
            required=["instance_id", "name", "organizations"]
        )
    )
    @action(methods=['post'], detail=False, url_path='update_monitor_instance')
    def update_monitor_instance(self, request):
        MonitorObjectService.update_instance(
            request.data.get("instance_id"),
            request.data.get("name"),
            request.data.get("organizations", []),
        )
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="instances_remove_organizations",
        operation_description="删除监控对象实例组织",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "instance_ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="监控实例ID列表"),
                "organizations": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="组织ID列表"),
            },
            required=["instance_ids", "organizations"]
        )
    )
    @action(methods=['post'], detail=False, url_path='instances_remove_organizations')
    def instances_remove_organizations(self, request):
        """删除监控对象实例组织"""
        instance_ids = request.data.get("instance_ids", [])
        organizations = request.data.get("organizations", [])
        MonitorObjectService.remove_instances_organizations(instance_ids, organizations)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="instances_add_organizations",
        operation_description="添加监控对象实例组织",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "instance_ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="监控实例ID列表"),
                "organizations": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="组织ID列表"),
            },
            required=["instance_ids", "organizations"]
        )
    )
    @action(methods=['post'], detail=False, url_path='instances_add_organizations')
    def instances_add_organizations(self, request):
        """添加监控对象实例组织"""
        instance_ids = request.data.get("instance_ids", [])
        organizations = request.data.get("organizations", [])
        MonitorObjectService.add_instances_organizations(instance_ids, organizations)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="set_instances_organizations",
        operation_description="设置监控对象实例组织",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "instance_ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),
                                               description="监控实例ID列表"),
                "organizations": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),
                                                description="组织ID列表"),
            },
            required=["instance_ids", "organizations"]
        )
    )
    @action(methods=['post'], detail=False, url_path='set_instances_organizations')
    def set_instances_organizations(self, request):
        """设置监控对象实例组织"""
        instance_ids = request.data.get("instance_ids", [])
        organizations = request.data.get("organizations", [])
        MonitorObjectService.set_instances_organizations(instance_ids, organizations)
        return WebUtils.response_success()