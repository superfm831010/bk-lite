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

        # permission = get_permission_rules(
        #     request.user,
        #     request.COOKIES.get("current_team"),
        #     "log",
        #     f"{POLICY_MODULE}.{collect_type_id}",
        # )
        # qs = permission_filter(Policy, permission, team_key="organizations__in", id_key="id__in")

        qs = Policy.objects.filter(collect_type_id=collect_type_id)

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

        # # 如果有权限规则，则添加到数据中
        # inst_permission_map = {i["id"]: i["permission"] for i in permission.get("instance", [])}
        #
        # for instance_info in results:
        #     if instance_info['id'] in inst_permission_map:
        #         instance_info['permission'] = inst_permission_map[instance_info['id']]
        #     else:
        #         instance_info['permission'] = DEFAULT_PERMISSION

        return WebUtils.response_success(dict(count=queryset.count(), items=results))

    def create(self, request, *args, **kwargs):
        # 补充创建人
        request.data['created_by'] = request.user.username
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
        pass
        # task_name = f'log_policy_task_{policy_id}'
        #
        # # 删除旧的定时任务
        # PeriodicTask.objects.filter(name=task_name).delete()
        #
        # # 解析 schedule，并创建相应的调度
        # format_crontab = self.format_crontab(schedule)
        # # 创建新的 PeriodicTask
        # PeriodicTask.objects.create(
        #     name=task_name,
        #     task='apps.log.tasks.execute_policy_task',
        #     args=json.dumps([policy_id]),
        #     crontab=format_crontab,
        #     enabled=True
        # )

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

    @swagger_auto_schema(
        operation_id="policy_test",
        operation_description="测试策略配置",
    )
    @action(methods=['post'], detail=True, url_path='test')
    def test(self, request, pk=None):
        policy = self.get_object()
        # TODO: 实现策略测试逻辑
        return WebUtils.response_success({"message": "策略测试功能待实现"})


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    filterset_class = AlertFilter
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Alert.objects.select_related('policy', 'collect_type').order_by('-created_at')

    @swagger_auto_schema(
        operation_id="alert_acknowledge",
        operation_description="确认告警",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "operator": openapi.Schema(type=openapi.TYPE_STRING, description="处理人")
            }
        )
    )
    @action(methods=['post'], detail=True, url_path='acknowledge')
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        operator = request.data.get('operator', request.user.username)

        alert.status = 'acknowledged'
        alert.operator = operator
        alert.save()

        return WebUtils.response_success({"status": "acknowledged", "operator": operator})

    @swagger_auto_schema(
        operation_id="alert_resolve",
        operation_description="解决告警",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "operator": openapi.Schema(type=openapi.TYPE_STRING, description="处理人")
            }
        )
    )
    @action(methods=['post'], detail=True, url_path='resolve')
    def resolve(self, request, pk=None):
        alert = self.get_object()
        operator = request.data.get('operator', request.user.username)

        alert.status = 'resolved'
        alert.operator = operator
        alert.save()

        return WebUtils.response_success({"status": "resolved", "operator": operator})


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
