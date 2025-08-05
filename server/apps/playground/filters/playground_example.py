from django_filters import rest_framework as filters
from apps.playground.models.playground_example import PlayGroundFile

class PlayGroundExampleFilter(filters.FilterSet):
    """
    PlayGroundFile过滤器 支持capability字段过滤，name模糊查询
    """
    name = filters.CharFilter(lookup_expr='icontains', label='文件名称模糊查询')
    capability = filters.CharFilter(field_name='capability_id',label='能力类型')
    is_active = filters.BooleanFilter(label='是否启用')

    class Meta:
        model = PlayGroundFile
        fields = ['name', 'capability']