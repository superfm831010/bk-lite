import toml
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.core.utils.web_utils import WebUtils
from apps.log.models.collect_config import CollectType, CollectInstance, CollectConfig
from apps.log.serializers.collect_config import CollectTypeSerializer
from apps.log.filters.collect_config import CollectTypeFilter
from apps.log.services.collect_type import CollectTypeService
from apps.rpc.node_mgmt import NodeMgmt


class CollectTypeViewSet(ModelViewSet):
    queryset = CollectType.objects.all()
    serializer_class = CollectTypeSerializer
    filterset_class = CollectTypeFilter


class CollectInstanceViewSet(ViewSet):

    @swagger_auto_schema(
        operation_description="查询采集实例列表",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "collect_type_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="采集类型ID"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="采集实例名称"),
                "page": openapi.Schema(type=openapi.TYPE_INTEGER, description="页码"),
                "page_size": openapi.Schema(type=openapi.TYPE_INTEGER, description="每页数据条数"),
            },
            required=["page", "page_size"]
        ),
    )
    @action(methods=['post'], detail=False, url_path='search')
    def search(self, request):
        """
        List all collect instances.
        """
        collect_type_id = request.query_params.get("collect_type_id")
        name = request.query_params.get("name")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))

        data = CollectTypeService.search_instance(
            collect_type_id=collect_type_id,
            name=name,
            page=page,
            page_size=page_size
        )

        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="批量接入日志",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "collector": openapi.Schema(type=openapi.TYPE_STRING, description="采集器名称"),
                "collect_type": openapi.Schema(type=openapi.TYPE_STRING, description="采集类型"),
                "collect_type_id": openapi.Schema(type=openapi.TYPE_NUMBER, description="采集类型ID"),
                "configs": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "...": openapi.Schema(type=openapi.TYPE_STRING, description="公共配置内容"),
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
            required=["collector", "collect_type_id", "collect_type", "configs", "instances"]
        )
    )
    @action(methods=['post'], detail=False, url_path='batch_create')
    def batch_create(self, request):
        CollectTypeService.batch_create_collect_configs(request.data)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="remove_collect_instance",
        operation_description="批量删除采集实例",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "instance_ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),
                                               description="采集实例ID列表"),
            },
            required=["instance_ids"]
        )
    )
    @action(methods=['post'], detail=False, url_path='remove_collect_instance')
    def remove_collect_instance(self, request):
        instance_ids = request.data.get("instance_ids", [])
        config_objs = CollectConfig.objects.filter(collect_instance_id__in=instance_ids)
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
        CollectInstance.objects.filter(id__in=instance_ids).delete()
        return WebUtils.response_success()


    @swagger_auto_schema(
        operation_id="instance_update",
        operation_description="更新实例",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "instance_id": openapi.Schema(type=openapi.TYPE_STRING, description="实例ID"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="实例名称"),
                "organizations": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER, description="组织ID列表")
                ),
            },
            required=["instance_id", "name", "organizations"]
        )
    )
    @action(methods=['post'], detail=False, url_path='instance_update')
    def instance_update(self, request):
        CollectTypeService.update_instance(
            request.data.get("instance_id"),
            request.data.get("name"),
            request.data.get("organizations", []),
        )
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="set_organizations",
        operation_description="设置实例组织",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "instance_ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),
                                               description="实例ID列表"),
                "organizations": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),
                                                description="组织ID列表"),
            },
            required=["instance_ids", "organizations"]
        )
    )
    @action(methods=['post'], detail=False, url_path='set_organizations')
    def set_organizations(self, request):
        """设置监控对象实例组织"""
        instance_ids = request.data.get("instance_ids", [])
        organizations = request.data.get("organizations", [])
        CollectTypeService.set_instances_organizations(instance_ids, organizations)
        return WebUtils.response_success()


class CollectConfigViewSet(ViewSet):

    @swagger_auto_schema(
        operation_description="查询配置内容",
        operation_id="get_config_content",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),
                                      description="配置ID列表"),
            },
            required=["ids"]
        ),
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

            config["content"] = toml.loads(config[content_key])

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
    )
    @action(methods=['post'], detail=False, url_path='update_instance_collect_config')
    def update_instance_collect_config(self, request):
        CollectTypeService.update_instance_config(request.data.get("child"), request.data.get("base"))
        return WebUtils.response_success()
