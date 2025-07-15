from django_filters import rest_framework as filters
from apps.playground.models.playground_capability import PlayGroundCapability

class PlayGroundCapabilityFilter(filters.FilterSet):
    """
    PlayGroundCapability 的过滤器，支持按名称、分类、是否启用等字段过滤。
    """
    name = filters.CharFilter(lookup_expr='icontains', label='名称模糊查询')
    category = filters.NumberFilter(field_name='category_id', label='分类ID')
    is_active = filters.BooleanFilter(label='是否启用')

    class Meta:
        model = PlayGroundCapability
        fields = ['name', 'category', 'is_active']
