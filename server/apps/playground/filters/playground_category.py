from django_filters import rest_framework as filters
from apps.playground.models.playground_category import PlayGroundCategory

class PlayGroundCategoryFilter(filters.FilterSet):
    """
    PlayGroundCategory 的过滤器，支持按名称、父分类等字段过滤。
    """
    name = filters.CharFilter(lookup_expr='icontains', label='名称模糊查询')
    parent = filters.NumberFilter(field_name='parent_id', label='父分类ID')

    class Meta:
        model = PlayGroundCategory
        fields = ['name', 'parent']
