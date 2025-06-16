from datetime import datetime, timedelta, timezone

from django_filters import rest_framework as filters

from apps.node_mgmt.models.sidecar import Node


class NodeFilter(filters.FilterSet):
    id = filters.CharFilter(field_name='id', lookup_expr='exact', label='节点ID')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains', label='节点名称')
    ip = filters.CharFilter(field_name='ip', lookup_expr='icontains', label='IP地址')
    operating_system = filters.CharFilter(field_name='operating_system', lookup_expr='exact', label='操作系统')
    cloud_region_id = filters.CharFilter(field_name='cloud_region_id', lookup_expr='exact', label='云区域ID')
    is_active = filters.BooleanFilter(method='filter_is_active', label='是否活跃')

    def filter_is_active(self, queryset, name, value):
        now = datetime.now(timezone.utc)
        threshold = now - timedelta(minutes=1)
        if value:  # True 表示活跃
            return queryset.filter(updated_at__gte=threshold)
        else:  # False 表示非活跃
            return queryset.filter(updated_at__lt=threshold)

    class Meta:
        model = Node
        fields = ['id', 'name', 'ip', 'operating_system', 'cloud_region_id']
