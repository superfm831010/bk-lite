from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from apps.core.utils.open_base import OpenAPIViewSet
from apps.node_mgmt.services.sidecar import Sidecar
from apps.node_mgmt.utils.token_auth import token_auth


class OpenSidecarViewSet(OpenAPIViewSet):
    @swagger_auto_schema(
        operation_id="sidecar_server_info",
        operation_description="获取服务器信息",
    )
    @action(detail=False, methods=["get"], url_path="node")
    @token_auth
    def server_info(self, request):
        return Sidecar.get_version()

    @swagger_auto_schema(
        operation_id="sidecar_collectors",
        operation_description="获取采集器列表",
    )
    @action(detail=False, methods=["get"], url_path="node/sidecar/collectors")
    @token_auth
    def collectors(self, request):
        return Sidecar.get_collectors(request)

    @swagger_auto_schema(
        operation_id="sidecar_node_configuration",
        operation_description="获取节点配置",
        manual_parameters=[
            openapi.Parameter("node_id", openapi.IN_PATH, description="节点ID", type=openapi.TYPE_STRING),
            openapi.Parameter("configuration_id", openapi.IN_PATH, description="配置ID", type=openapi.TYPE_STRING),
        ],
    )
    @action(detail=False, methods=["get"],
            url_path="node/sidecar/configurations/render/(?P<node_id>.+?)/(?P<configuration_id>.+?)")
    @token_auth
    def configuration(self, request, node_id, configuration_id):
        return Sidecar.get_node_config(request, node_id, configuration_id)

    @swagger_auto_schema(
        operation_id="sidecar_node_configuration_env",
        operation_description="获取配置关联的环境变量配置",
        manual_parameters=[
            openapi.Parameter("node_id", openapi.IN_PATH, description="节点ID", type=openapi.TYPE_STRING),
            openapi.Parameter("configuration_id", openapi.IN_PATH, description="配置ID", type=openapi.TYPE_STRING),
        ],
    )
    @action(detail=False, methods=["get"],
            url_path="node/sidecar/env_config/(?P<node_id>.+?)/(?P<configuration_id>.+?)")
    @token_auth
    def configuration_env(self, request, node_id, configuration_id):
        return Sidecar.get_node_config_env(node_id, configuration_id)

    @swagger_auto_schema(
        operation_id="sidecar_update_client",
        operation_description="更新sidecar客户端",
        manual_parameters=[
            openapi.Parameter("node_id", openapi.IN_PATH, description="节点ID", type=openapi.TYPE_STRING)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "node_name": openapi.Schema(type=openapi.TYPE_STRING, description="节点名称"),
                "node_details": openapi.Schema(type=openapi.TYPE_OBJECT, description="节点详情"),
            },
        ),
    )
    @action(detail=False, methods=["PUT"], url_path="node/sidecars/(?P<node_id>.+?)")
    @token_auth
    def update_sidecar_client(self, request, node_id):
        return Sidecar.update_node_client(request, node_id)
