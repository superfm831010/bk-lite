import toml
import yaml
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.core.utils.web_utils import WebUtils
from apps.log.models import CollectType, CollectInstance, CollectConfig
from apps.log.serializers.collect_config import CollectTypeSerializer
from apps.log.filters.collect_config import CollectTypeFilter
from apps.log.services.collect_type import CollectTypeService
from apps.rpc.node_mgmt import NodeMgmt


class CollectTypeViewSet(ModelViewSet):
    queryset = CollectType.objects.all()
    serializer_class = CollectTypeSerializer
    filterset_class = CollectTypeFilter

    @swagger_auto_schema(
        operation_description="获取采集类型列表",
        manual_parameters=[
            openapi.Parameter(
                'add_policy_count',
                openapi.IN_QUERY,
                description="是否计算采集类型下的策略数量统计",
                type=openapi.TYPE_BOOLEAN,
                default=False,
                required=False
            ),
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="按名称模糊搜索",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'collector',
                openapi.IN_QUERY,
                description="按采集器名称模糊搜索",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        获取采集类型列表

        支持参数：
        - add_policy_count: 是否计算策略数量，true/false，默认false
        - name: 按名称模糊搜索
        - collector: 按采集器名称模糊搜索
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="获取所有采集类型的属性",
        operation_id="get_all_attrs",
    )
    @action(methods=['get'], detail=False, url_path='all_attrs')
    def get_all_attrs(self, request):
        """
        获取所有采集类型的属性，并进行去重
        """
        # 获取所有采集类型的属性列表
        collect_types = CollectType.objects.all()

        # 收集所有属性并去重
        all_attrs = set()
        for collect_type in collect_types:
            if collect_type.attrs and isinstance(collect_type.attrs, list):
                all_attrs.update(collect_type.attrs)

        # 转换为排序的列表，保证返回结果的一致性
        unique_attrs = sorted(list(all_attrs))

        return WebUtils.response_success(unique_attrs)


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
        collect_type_id = request.data.get("collect_type_id")
        name = request.data.get("name")
        page = int(request.data.get("page", 1))
        page_size = int(request.data.get("page_size", 10))

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

            if config_obj.file_type == "yaml":
                config["content"] = yaml.safe_load(config[content_key])
            else:
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
                "instance_id": openapi.Schema(type=openapi.TYPE_STRING, description="采集实例ID"),
                "collect_type_id": openapi.Schema(type=openapi.TYPE_STRING, description="采集类型ID"),
                "child": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING, description="配置ID"),
                        "content_data": openapi.Schema(type=openapi.TYPE_OBJECT, description="配置内容"),
                    },
                ),
                "base": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING, description="配置ID"),
                        "content_data": openapi.Schema(type=openapi.TYPE_OBJECT, description="配置内容"),
                        "env_config": openapi.Schema(type=openapi.TYPE_OBJECT, description="环境变量配置"),
                    },
                ),
            },
        ),
    )
    @action(methods=['post'], detail=False, url_path='update_instance_collect_config')
    def update_instance_collect_config(self, request):
        CollectTypeService.update_instance_config_v2(
            request.data.get("child"),
            request.data.get("base"),
            request.data.get("instance_id"),
            request.data.get("collect_type_id"),
        )
        return WebUtils.response_success()
