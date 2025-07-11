from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from apps.core.utils.web_utils import WebUtils
from apps.rpc.node_mgmt import NodeMgmt


class NodeViewSet(ViewSet):
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
        organization_ids = [] if request.user.is_superuser else [i["id"] for i in request.user.group_list]
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
