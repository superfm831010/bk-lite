from rest_framework import mixins
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.node_mgmt.filters.cloud_region import CloudRegionFilter
from apps.node_mgmt.models import Node
from apps.node_mgmt.serializers.cloud_region import CloudRegionSerializer, CloudRegionUpdateSerializer
from apps.node_mgmt.models.cloud_region import CloudRegion
from drf_yasg import openapi


class CloudRegionViewSet(mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.CreateModelMixin,
                         GenericViewSet):
    queryset = CloudRegion.objects.all()
    serializer_class = CloudRegionSerializer
    filterset_class = CloudRegionFilter
    search_fields = ['name', 'introduction']  # 搜索字段

    @swagger_auto_schema(
        operation_summary="获取云区域列表",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="模糊搜索(name, introduction)",
                              type=openapi.TYPE_STRING),
        ],
        tags=['CloudRegion']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="部分更新云区域",
        tags=['CloudRegion'],
        request_body=CloudRegionUpdateSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = CloudRegionUpdateSerializer
        # 默认云区域default禁止编辑
        cloud_region_id = kwargs.get('pk')
        cloud_region = CloudRegion.objects.filter(id=cloud_region_id).first()
        if cloud_region and cloud_region.name == 'default':
            raise BaseAppException("默认云区域禁止编辑")
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="创建云区域",
        tags=['CloudRegion'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="云区域名称"),
                'introduction': openapi.Schema(type=openapi.TYPE_STRING, description="云区域介绍"),
            }
        ),
    )
    def create(self, request, *args, **kwargs):
        self.serializer_class = CloudRegionSerializer
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="删除云区域",
        tags=['CloudRegion'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="云区域ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        # 校验云区域下是否存在节点
        cloud_region_id = kwargs.get('pk')
        if Node.objects.filter(cloud_region_id=cloud_region_id).exists():
            raise BaseAppException("该云区域下存在节点，无法删除")
        return super().destroy(request, *args, **kwargs)
