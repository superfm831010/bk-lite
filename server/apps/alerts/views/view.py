# -- coding: utf-8 --
# @File: view.py
# @Time: 2025/5/9 15:14
# @Author: windyzhao
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import Count

from apps.alerts.filters import AlertSourceModelFilter, AlertModelFilter
from apps.alerts.models import AlertSource, Alert
from apps.alerts.serializers.serializers import AlertSourceModelSerializer, AlertModelSerializer
from apps.core.utils.web_utils import WebUtils
from config.drf.pagination import CustomPageNumberPagination
from config.drf.viewsets import ModelViewSet


def request_test(requests):
    """
    Test function to handle requests.

    :param requests: The request data.
    :return: A response indicating success or failure.
    """
    print("Processing request:", requests)
    return WebUtils.response_success([])


class AlertSourceModelViewSet(ModelViewSet):
    queryset = AlertSource.objects.all()
    serializer_class = AlertSourceModelSerializer
    ordering_fields = ["updated_at"]
    ordering = ["-updated_at"]
    filterset_class = AlertSourceModelFilter
    pagination_class = CustomPageNumberPagination


class AlterModelViewSet(ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertModelSerializer
    ordering_fields = ["updated_at"]
    ordering = ["-updated_at"]
    filterset_class = AlertModelFilter
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Alert.objects.annotate(
            event_count_annotated=Count('event_set'),
            source_names_annotated=StringAgg('source__name', delimiter=', ', distinct=True)
        ).prefetch_related('source')

    def list(self, request, *args, **kwargs):
        """
        List all alerts with optional filtering and pagination.
        """
        return super().list(request, *args, **kwargs)
