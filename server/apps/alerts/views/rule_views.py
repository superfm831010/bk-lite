from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch

from apps.alerts.filters import CorrelationRulesModelFilter, AggregationRulesModelFilter
from apps.alerts.models import AggregationRules, CorrelationRules
from apps.alerts.serializers.rule_serializers import AggregationRulesSerializer, CorrelationRulesSerializer
from config.drf.pagination import CustomPageNumberPagination
from apps.core.logger import alert_logger as logger


class AggregationRulesViewSet(viewsets.ModelViewSet):
    """聚合规则视图集"""

    queryset = AggregationRules.objects.filter(is_active=True)
    serializer_class = AggregationRulesSerializer
    filterset_class = AggregationRulesModelFilter
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """获取聚合规则查询集，预加载关联规则数据"""
        return AggregationRules.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                'correlation_rules',
                queryset=CorrelationRules.objects.only('name'),
                to_attr='related_rules_names'
            )
        )

    @action(detail=False, methods=['post'])
    def reload_rules(self, request):
        """重新加载数据库规则到告警引擎"""
        try:
            # 移动导入到函数内部避免循环导入
            from apps.alerts.common.aggregation.alert_processor import AlertProcessor
            processor = AlertProcessor()
            processor.reload_database_rules()

            # 统计加载的规则数量
            rule_count = AggregationRules.objects.filter(is_active=True).count()

            return Response({
                'success': True,
                'message': f'成功重新加载 {rule_count} 个规则到告警引擎',
                'rule_count': rule_count
            })
        except Exception as e:
            logger.error(f"重新加载规则失败: {str(e)}")
            return Response({
                'success': False,
                'message': f'重新加载规则失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CorrelationRulesViewSet(viewsets.ModelViewSet):
    """关联规则视图集"""

    queryset = CorrelationRules.objects.all()
    serializer_class = CorrelationRulesSerializer
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    filterset_class = CorrelationRulesModelFilter
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """获取关联规则查询集，预加载聚合规则数据"""
        return CorrelationRules.objects.prefetch_related(
            Prefetch(
                'aggregation_rules',
                queryset=AggregationRules.objects.only('name'),
                to_attr='related_rules_names'
            )
        )

    def create(self, request, *args, **kwargs):
        """创建关联规则"""
        aggregation_rules = request.data["aggregation_rules"]
        if not aggregation_rules:
            return Response(
                {"detail": "必须提供至少一个聚合规则来创建关联规则。"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if CorrelationRules.objects.filter(aggregation_rules__in=aggregation_rules).exists():
            return Response(
                {"detail": "所选聚合规则已被其他关联规则使用，请选择其他聚合规则。"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)
