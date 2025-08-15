import json

from django_celery_beat.models import PeriodicTask, CrontabSchedule
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.core.utils.permission_utils import get_permission_rules, permission_filter
from apps.core.utils.web_utils import WebUtils
from apps.log.constants import POLICY_MODULE, DEFAULT_PERMISSION
from apps.log.filters.policy import PolicyFilter, AlertFilter, EventFilter
from apps.log.models.policy import Policy, Alert, Event, EventRawData
from apps.log.serializers.policy import PolicySerializer, AlertSerializer, EventSerializer, EventRawDataSerializer
from config.drf.pagination import CustomPageNumberPagination


class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    filterset_class = PolicyFilter
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):
        collect_type_id = request.query_params.get('collect_type', None)

        # 获取权限规则
        permission = get_permission_rules(
            request.user,
            request.COOKIES.get("current_team"),
            "log",
            f"{POLICY_MODULE}.{collect_type_id}",
        )

        # 应用权限过滤
        base_qs = permission_filter(
            Policy,
            permission,
            team_key="policyorganization__organization__in",
            id_key="id__in"
        )

        # 基于collect_type和当前团队过滤
        qs = base_qs.filter(
            collect_type_id=collect_type_id,
            policyorganization__organization=request.COOKIES.get("current_team")
        )

        queryset = self.filter_queryset(qs)
        queryset = queryset.distinct().select_related('collect_type')

        # 获取分页参数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        # 计算分页的起始位置
        start = (page - 1) * page_size
        end = start + page_size

        # 获取当前页的数据
        page_data = queryset[start:end]

        # 执行序列化
        serializer = self.get_serializer(page_data, many=True)
        results = serializer.data

        # 添加权限信息到每个策略实例
        policy_permission_map = {i["id"]: i["permission"] for i in permission.get("instance", [])}

        for policy_info in results:
            if policy_info['id'] in policy_permission_map:
                policy_info['permission'] = policy_permission_map[policy_info['id']]
            else:
                policy_info['permission'] = DEFAULT_PERMISSION

        return WebUtils.response_success(dict(count=queryset.count(), items=results))

    def create(self, request, *args, **kwargs):
        # 补充创建人
        request.data['created_by'] = request.user.username
        request.data['updated_by'] = request.user.username
        response = super().create(request, *args, **kwargs)
        policy_id = response.data['id']
        schedule = request.data.get('schedule')
        if schedule:
            self.update_or_create_task(policy_id, schedule)
        return response

    def update(self, request, *args, **kwargs):
        # 补充更新人
        request.data['updated_by'] = request.user.username
        response = super().update(request, *args, **kwargs)
        policy_id = kwargs['pk']
        schedule = request.data.get('schedule')
        if schedule:
            self.update_or_create_task(policy_id, schedule)
        return response

    def partial_update(self, request, *args, **kwargs):
        # 补充更新人
        request.data['updated_by'] = request.user.username
        response = super().partial_update(request, *args, **kwargs)
        policy_id = kwargs['pk']
        schedule = request.data.get('schedule')
        if schedule:
            self.update_or_create_task(policy_id, schedule)
        return response

    def destroy(self, request, *args, **kwargs):
        policy_id = kwargs['pk']
        # 删除相关的定时任务
        PeriodicTask.objects.filter(name=f'log_policy_task_{policy_id}').delete()
        return super().destroy(request, *args, **kwargs)

    def format_crontab(self, schedule):
        """
        将 schedule 格式化为 CrontabSchedule 实例
        """
        schedule_type = schedule.get('type')
        value = schedule.get('value')

        if schedule_type == 'min':
            return CrontabSchedule.objects.get_or_create(
                minute=f'*/{value}', hour='*', day_of_month='*', month_of_year='*', day_of_week='*'
            )[0]
        elif schedule_type == 'hour':
            return CrontabSchedule.objects.get_or_create(
                minute=0, hour=f'*/{value}', day_of_month='*', month_of_year='*', day_of_week='*'
            )[0]
        elif schedule_type == 'day':
            return CrontabSchedule.objects.get_or_create(
                minute=0, hour=0, day_of_month=f'*/{value}', month_of_year='*', day_of_week='*'
            )[0]
        else:
            raise BaseAppException('Invalid schedule type')

    def update_or_create_task(self, policy_id, schedule):
        task_name = f'log_policy_task_{policy_id}'

        # 删除旧的定时任务
        PeriodicTask.objects.filter(name=task_name).delete()

        # 解析 schedule，并创建相应的调度
        format_crontab = self.format_crontab(schedule)
        # 创建新的 PeriodicTask
        PeriodicTask.objects.create(
            name=task_name,
            task='apps.log.tasks.policy.scan_log_policy_task',
            args=json.dumps([policy_id]),
            crontab=format_crontab,
            enabled=True
        )

    @swagger_auto_schema(
        operation_id="policy_enable",
        operation_description="启用/禁用策略",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "enabled": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否启用")
            },
            required=["enabled"]
        )
    )
    @action(methods=['post'], detail=True, url_path='enable')
    def enable(self, request, pk=None):
        policy = self.get_object()
        enabled = request.data.get('enabled', True)

        task_name = f'log_policy_task_{pk}'
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.enabled = enabled
            task.save()
            return WebUtils.response_success({"enabled": enabled})
        except PeriodicTask.DoesNotExist:
            return WebUtils.response_error("策略对应的定时任务不存在")


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.select_related('policy', 'collect_type').order_by('-created_at')
    serializer_class = AlertSerializer
    filterset_class = AlertFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="alert_list",
        operation_description="告警列表查询",
        manual_parameters=[
            openapi.Parameter('levels', openapi.IN_QUERY, description="告警级别多选，用逗号分隔，如：critical,warning,info", type=openapi.TYPE_STRING),
            openapi.Parameter('content', openapi.IN_QUERY, description="告警内容关键字搜索", type=openapi.TYPE_STRING),
            openapi.Parameter('collect_type', openapi.IN_QUERY, description="采集类型ID", type=openapi.TYPE_INTEGER, required=True),
        ],
    )
    def list(self, request, *args, **kwargs):
        collect_type_id = request.query_params.get('collect_type', None)
        if not collect_type_id:
            return WebUtils.response_error("collect_type is required")

        # 获取policy模块的权限规则
        permission = get_permission_rules(
            request.user,
            request.COOKIES.get("current_team"),
            "log",
            f"{POLICY_MODULE}.{collect_type_id}",
        )

        # 先过滤出有权限的Policy
        policy_qs = permission_filter(
            Policy,
            permission,
            team_key="policyorganization__organization__in",
            id_key="id__in"
        )
        policy_qs = policy_qs.filter(
            collect_type_id=collect_type_id,
            policyorganization__organization=request.COOKIES.get("current_team")
        ).distinct()

        # 获取有权限的policy_ids
        policy_ids = list(policy_qs.values_list("id", flat=True))

        # 基于policy权限过滤告警
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(policy_id__in=policy_ids).distinct()

        # 分页处理
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        results = serializer.data

        # 添加权限信息到每个告警
        policy_permission_map = {i["id"]: i["permission"] for i in permission.get("instance", [])}

        for alert_info in results:
            policy_id = alert_info.get("policy")
            if policy_id in policy_permission_map:
                alert_info["permission"] = policy_permission_map[policy_id]
            else:
                alert_info["permission"] = DEFAULT_PERMISSION

        return self.get_paginated_response(results)

    @swagger_auto_schema(
        operation_id="alert_closed",
        operation_description="关闭告警",
    )
    @action(methods=['post'], detail=True, url_path='closed')
    def closed(self, request, pk=None):
        alert = self.get_object()
        operator = request.user.username

        alert.status = 'closed'
        alert.operator = operator
        alert.save()

        return WebUtils.response_success({"status": "closed", "operator": operator})

    @swagger_auto_schema(
        operation_description="获取最新告警事件",
        operation_id="get_last_event_by_alert",
        manual_parameters=[
            openapi.Parameter('alert_id', openapi.IN_QUERY, description="告警ID", type=openapi.TYPE_STRING)
        ]
    )
    @action(methods=['get'], detail=False, url_path='last_event')
    def get_last_event(self, request):
        """
        获取最新的事件
        """
        alert_id = request.query_params.get('alert_id')
        if not alert_id:
            return WebUtils.response_error("缺少告警ID参数")

        event = Event.objects.filter(alert_id=alert_id).order_by('-event_time').first()
        if not event:
            return WebUtils.response_error("未找到相关事件")

        event_raw_data = EventRawData.objects.filter(event_id=event.id).first()

        data = {
            "event": EventSerializer(event).data,
            "raw_data": EventRawDataSerializer(event_raw_data).data if event_raw_data else None
        }

        return WebUtils.response_success(data)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Event.objects.select_related('policy', 'alert').order_by('-event_time')


class EventRawDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EventRawData.objects.all()
    serializer_class = EventRawDataSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return EventRawData.objects.select_related('event').order_by('-id')
