from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.utils.web_utils import WebUtils
from apps.monitor.filters.monitor_metrics import MetricGroupFilter, MetricFilter
from apps.monitor.language.service import SettingLanguage
from apps.monitor.serializers.monitor_metrics import MetricGroupSerializer, MetricSerializer
from apps.monitor.models.monitor_metrics import MetricGroup, Metric
from config.drf.pagination import CustomPageNumberPagination


class MetricGroupVieSet(viewsets.ModelViewSet):
    queryset = MetricGroup.objects.select_related('monitor_object').all().order_by("sort_order")
    serializer_class = MetricGroupSerializer
    filterset_class = MetricGroupFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="metrics_group_list",
        operation_description="指标分组列表",
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        results = serializer.data
        lan = SettingLanguage(request.user.locale)

        # 创建queryset字典缓存，避免重复查询
        queryset_dict = {obj.id: obj for obj in queryset}

        # 批量获取所有监控对象名称对应的语言配置
        monitor_object_names = set()
        for result in results:
            if result.get("monitor_object"):
                metric_group = queryset_dict.get(result["id"])
                if metric_group and metric_group.monitor_object:
                    monitor_object_names.add(metric_group.monitor_object.name)

        # 批量获取语言配置映射
        metric_group_maps = {}
        for monitor_object_name in monitor_object_names:
            metric_group_map = lan.get_val("MONITOR_OBJECT_METRIC_GROUP", monitor_object_name)
            if metric_group_map:
                metric_group_maps[monitor_object_name] = metric_group_map

        # 应用语言配置
        for result in results:
            if result.get("monitor_object"):
                metric_group = queryset_dict.get(result["id"])
                if metric_group and metric_group.monitor_object:
                    monitor_object_name = metric_group.monitor_object.name
                    metric_group_map = metric_group_maps.get(monitor_object_name, {})
                    result["display_name"] = metric_group_map.get(result["name"]) or result["name"]

        return WebUtils.response_success(results)

    @swagger_auto_schema(
        operation_id="metrics_group_create",
        operation_description="创建指标分组",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_update",
        operation_description="更新指标分组",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_partial_update",
        operation_description="部分更新指标分组",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_retrieve",
        operation_description="查询指标分组",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_del",
        operation_description="删除指标分组",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_set_order",
        operation_description="指标分组排序",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="指标分组ID"),
                    "sort_order": openapi.Schema(type=openapi.TYPE_INTEGER, description="排序"),
                }
            )
        )
    )
    @action(detail=False, methods=["post"])
    def set_order(self, request, *args, **kwargs):
        updates = [
            MetricGroup(
                id=item["id"],
                sort_order=item["sort_order"],
            )
            for item in request.data
        ]
        MetricGroup.objects.bulk_update(updates, ["sort_order"], batch_size=200)
        return WebUtils.response_success()


class MetricVieSet(viewsets.ModelViewSet):
    queryset = Metric.objects.select_related('monitor_object').all().order_by("sort_order")
    serializer_class = MetricSerializer
    filterset_class = MetricFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="metrics_list",
        operation_description="指标列表",
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        results = serializer.data
        lan = SettingLanguage(request.user.locale)

        # 批量获取所有监控对象名称对应的语言配置
        monitor_object_names = set()
        queryset_dict = {obj.id: obj for obj in queryset}

        for result in results:
            if result.get("monitor_object"):
                metric = queryset_dict.get(result["id"])
                if metric and metric.monitor_object:
                    monitor_object_names.add(metric.monitor_object.name)

        # 批量获取语言配置映射
        metric_maps = {}
        for monitor_object_name in monitor_object_names:
            metric_map = lan.get_val("MONITOR_OBJECT_METRIC", monitor_object_name)
            if metric_map:
                metric_maps[monitor_object_name] = metric_map

        # 应用语言配置
        for result in results:
            if result.get("monitor_object"):
                metric = queryset_dict.get(result["id"])
                if metric and metric.monitor_object:
                    monitor_object_name = metric.monitor_object.name
                    metric_map = metric_maps.get(monitor_object_name, {})
                    metric_config = metric_map.get(result["name"], {})
                    result["display_name"] = metric_config.get("name") or result["display_name"]
                    result["display_description"] = metric_config.get("desc") or result["description"]

        return WebUtils.response_success(results)

    @swagger_auto_schema(
        operation_id="metrics_create",
        operation_description="创建指标",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_update",
        operation_description="更新指标",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_partial_update",
        operation_description="部分更新指标",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_retrieve",
        operation_description="查询指标",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_del",
        operation_description="删除指标",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_set_order",
        operation_description="指标排序",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="指标分组ID"),
                    "sort_order": openapi.Schema(type=openapi.TYPE_INTEGER, description="排序"),
                }
            )
        )
    )
    @action(detail=False, methods=["post"])
    def set_order(self, request, *args, **kwargs):
        updates = [
            Metric(
                id=item["id"],
                sort_order=item["sort_order"],
            )
            for item in request.data
        ]
        Metric.objects.bulk_update(updates, ["sort_order"], batch_size=200)
        return WebUtils.response_success()
