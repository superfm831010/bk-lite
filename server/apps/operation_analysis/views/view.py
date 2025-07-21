# -- coding: utf-8 --
# @File: view.py
# @Time: 2025/7/14 17:22
# @Author: windyzhao
from apps.core.utils.web_utils import WebUtils
from apps.operation_analysis.filters import DataSourceAPIModelFilter
from apps.operation_analysis.serializers import DataSourceAPIModelSerializer
from config.drf.pagination import CustomPageNumberPagination
from config.drf.viewsets import ModelViewSet
from apps.operation_analysis.models import DataSourceAPIModel


def request_test(requests):
    print("Processing request:", requests)
    return WebUtils.response_success([])


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
