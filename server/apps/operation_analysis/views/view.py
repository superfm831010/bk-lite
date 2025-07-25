# -- coding: utf-8 --
# @File: view.py
# @Time: 2025/7/14 17:22
# @Author: windyzhao
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.operation_analysis.common.get_nats_source_data import GetNatsData
from apps.operation_analysis.filters import DataSourceAPIModelFilter, DashboardModelFilter
from apps.operation_analysis.serializers import DataSourceAPIModelSerializer, DashboardModelSerializer
from config.drf.pagination import CustomPageNumberPagination
from config.drf.viewsets import ModelViewSet
from apps.operation_analysis.models import DataSourceAPIModel, Dashboard
from apps.core.logger import operation_analysis_logger as logger


class DataSourceAPIModelViewSet(ModelViewSet):
    """
    数据源
    """
    queryset = DataSourceAPIModel.objects.all()
    serializer_class = DataSourceAPIModelSerializer
    ordering_fields = ["id"]
    ordering = ["id"]
    filterset_class = DataSourceAPIModelFilter
    pagination_class = CustomPageNumberPagination

    @action(detail=False, methods=["post"], url_path=r"get_source_data/(?P<pk>[^/.]+)")
    def get_source_data(self, request, *args, **kwargs):
        instance = self.get_object()
        params = request.data
        namespace, path = instance.rest_api.split("/", 1)
        client = GetNatsData(namespace=namespace, path=path, params=params)
        try:
            result = client.get_data()
        except Exception as e:
            logger.error("获取数据源数据失败: {}".format(e))
            result = {}

        return Response(result.get("data", []))


class DashboardModelViewSet(ModelViewSet):
    """
    仪表盘
    """
    queryset = Dashboard.objects.all()
    serializer_class = DashboardModelSerializer
    ordering_fields = ["id"]
    ordering = ["id"]
    filterset_class = DashboardModelFilter
    pagination_class = CustomPageNumberPagination
