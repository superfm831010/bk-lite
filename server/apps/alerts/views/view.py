# -- coding: utf-8 --
# @File: view.py
# @Time: 2025/5/9 15:14
# @Author: windyzhao
import uuid

from django.contrib.postgres.aggregates import StringAgg
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.alerts.filters import AlertSourceModelFilter, AlertModelFilter, EventModelFilter, LevelModelFilter, \
    IncidentModelFilter
from apps.alerts.models import AlertSource, Alert, Event, Level, Incident
from apps.alerts.serializers.serializers import AlertSourceModelSerializer, AlertModelSerializer, EventModelSerializer, \
    LevelModelSerializer, IncidentModelSerializer
from apps.alerts.service.alter_operator import AlertOperator
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
    """
    告警源
    """
    queryset = AlertSource.objects.all()
    serializer_class = AlertSourceModelSerializer
    ordering_fields = ["id"]
    ordering = ["id"]
    filterset_class = AlertSourceModelFilter
    pagination_class = CustomPageNumberPagination


class AlterModelViewSet(ModelViewSet):
    """
    告警视图集
    """
    # -level 告警等级排序
    queryset = Alert.objects.all()
    serializer_class = AlertModelSerializer
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    filterset_class = AlertModelFilter
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Alert.objects.annotate(
            event_count_annotated=Count('events'),
            # 通过事件获取告警源名称（去重）
            source_names_annotated=StringAgg('events__source__name', delimiter=', ', distinct=True)
        ).prefetch_related('events__source')
        return queryset

    def list(self, request, *args, **kwargs):
        """
        List all alerts with optional filtering and pagination.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(methods=['post'], detail=False, url_path='operator/(?P<operator_action>[^/.]+)', url_name='operator')
    def operator(self, request, operator_action, *args, **kwargs):
        """
        Custom operator method to handle alert operations.
        """
        alert_id_list = request.data["alert_id"]
        operator = AlertOperator(user=self.request.user.username)
        result_list = {}
        status_list = []
        for alert_id in alert_id_list:
            result = operator.operate(action=operator_action, alert_id=alert_id, data=request.data)
            result_list[alert_id] = result
            status_list.append(result["result"])

        if all(status_list):
            return WebUtils.response_success(result_list)
        elif not all(status_list):
            return WebUtils.response_error(
                response_data=result_list,
                error_message="操作失败，请检查日志!",
                status_code=500
            )
        else:
            return WebUtils.response_success(response_data=result_list, message="部分操作成功")


class EventModelViewSet(ModelViewSet):
    """
    事件视图集
    """
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer
    ordering_fields = ["received_at"]
    ordering = ["-received_at"]
    filterset_class = EventModelFilter
    pagination_class = CustomPageNumberPagination


class LevelModelViewSet(ModelViewSet):
    """
    告警等级视图集
    """
    # TODO 创建的时候动态增加level_id 锁表
    queryset = Level.objects.all()
    serializer_class = LevelModelSerializer
    filterset_class = LevelModelFilter
    ordering_fields = ["level_id"]
    ordering = ["level_id"]
    pagination_class = CustomPageNumberPagination


class IncidentModelViewSet(ModelViewSet):
    """
    事故视图集
    """
    queryset = Incident.objects.all()
    serializer_class = IncidentModelSerializer
    ordering_fields = ["created_at", "id"]  # 允许按创建时间和ID排序 ?ordering=-id
    ordering = ["-created_at"]  # 默认按创建时间降序排序
    filterset_class = IncidentModelFilter
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Incident.objects.annotate(
            alert_count=Count('alert')
        ).prefetch_related('alert')
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        incident_id = f"INCIDENT-{uuid.uuid4().hex}"
        data["incident_id"] = incident_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
