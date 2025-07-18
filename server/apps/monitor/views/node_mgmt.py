from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.core.utils.web_utils import WebUtils
from apps.monitor.models import CollectConfig
from apps.monitor.services.node_mgmt import InstanceConfigService
from apps.monitor.utils.config_format import ConfigFormat
from apps.rpc.node_mgmt import NodeMgmt
from apps.core.logger import monitor_logger as logger


class NodeMgmtView(ViewSet):
    @swagger_auto_schema(
        operation_description="查询节点列表",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "cloud_region_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="云区域ID"),
                "page": openapi.Schema(type=openapi.TYPE_INTEGER, description="页码"),
                "page_size": openapi.Schema(type=openapi.TYPE_INTEGER, description="每页数据条数"),
                "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否活跃"),
            },
            required=["cloud_region_id", "page", "page_size"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='nodes')
    def get_nodes(self, request):

        orgs = {i["id"] for i in request.user.group_list if i["name"] == "OpsPilotGuest"}
        orgs.add(request.COOKIES.get("current_team"))

        organization_ids = [] if request.user.is_superuser else orgs
        data = NodeMgmt().node_list(dict(
            cloud_region_id=request.data.get("cloud_region_id", 1),
            organization_ids=organization_ids,
            name=request.data.get("name"),
            ip=request.data.get("ip"),
            os=request.data.get("os"),
            page=request.data.get("page", 1),
            page_size=request.data.get("page_size", 10),
            is_active=request.data.get("is_active")
        ))
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="批量设置节点子配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "monitor_object_id": openapi.Schema(type=openapi.TYPE_STRING, description="监控对象id"),
                "collector": openapi.Schema(type=openapi.TYPE_STRING, description="采集器名称"),
                "collect_type": openapi.Schema(type=openapi.TYPE_STRING, description="采集类型"),
                "configs": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "type": openapi.Schema(type=openapi.TYPE_STRING, description="配置类型"),
                            "...": openapi.Schema(type=openapi.TYPE_STRING, description="配置内容"),
                        }
                    )),
                "instances": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "instance_id": openapi.Schema(type=openapi.TYPE_STRING, description="实例id"),
                            "instance_type": openapi.Schema(type=openapi.TYPE_STRING, description="实例类型"),
                            "instance_name": openapi.Schema(type=openapi.TYPE_STRING, description="实例类型"),
                            "group_ids": openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER), description="组织id列表"),
                            "node_ids": openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER), description="节点id列表"),
                            "...": openapi.Schema(type=openapi.TYPE_OBJECT, description="其他信息"),
                        }
                    )
                )
            },
            required=["monitor_object_id", "collector", "collect_type", "configs", "instances"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='batch_setting_node_child_config')
    def batch_setting_node_child_config(self, request):
        logger.info(f"batch_setting_node_child_config: {request.data}")

        InstanceConfigService.create_monitor_instance_by_node_mgmt(request.data)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_description="查询实例关联的配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "instance_type": openapi.Schema(type=openapi.TYPE_STRING, description="采集实例类型"),
                "instance_id": openapi.Schema(type=openapi.TYPE_STRING, description="采集实例ID"),
            },
            required=["instance_type", "instance_id"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='get_instance_asso_config')
    def get_instance_child_config(self, request):
        data = InstanceConfigService.get_instance_configs(request.data["instance_id"], request.data["instance_type"])
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="查询配置内容",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="配置ID列表"),
            },
            required=["ids"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='get_config_content')
    def get_config_content(self, request):
        config_objs = CollectConfig.objects.filter(id__in=request.data["ids"])
        if not config_objs:
            return WebUtils.response_error("配置不存在!")

        result = {}
        for config_obj in config_objs:
            content_key = "content" if config_obj.is_child else "config_template"
            if config_obj.is_child:
                configs = NodeMgmt().get_child_configs_by_ids([config_obj.id])
            else:
                configs = NodeMgmt().get_configs_by_ids([config_obj.id])
            config = configs[0]
            if config_obj.file_type == "toml":
                config["content"] = ConfigFormat.toml_to_dict(config[content_key])
            elif config_obj.file_type == "yaml":
                config["content"] = ConfigFormat.yaml_to_dict(config[content_key])
            else:
                raise BaseAppException("file_type must be toml or yaml")
            if config_obj.is_child:
                result["child"] = config
            else:
                result["base"] = config

        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_description="更改采集配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "child": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING, description="配置ID"),
                        "content": openapi.Schema(type=openapi.TYPE_OBJECT, description="配置内容"),
                    },
                ),
                "base": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING, description="配置ID"),
                        "content": openapi.Schema(type=openapi.TYPE_OBJECT, description="配置内容"),
                        "env_config": openapi.Schema(type=openapi.TYPE_OBJECT, description="环境变量配置"),
                    },
                ),
            },
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='update_instance_collect_config')
    def update_instance_collect_config(self, request):
        InstanceConfigService.update_instance_config(request.data.get("child"), request.data.get("base"))
        return WebUtils.response_success()
