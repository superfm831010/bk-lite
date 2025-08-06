from django_filters import rest_framework as filters
from apps.playground.models.playground_example import PlaygroundAnomalyDetectionExample

class PlaygroundAnomalyDetectionExampleFilter(filters.FilterSet):
    """
    PlaygroundAnomalyDetectionExample过滤器 支持capability字段过滤，name模糊查询
    """
    name = filters.CharFilter(lookup_expr='icontains', label='文件名称模糊查询')
    capability = filters.CharFilter(field_name='capability',label='能力类型')
    is_active = filters.BooleanFilter(label='是否启用')

    class Meta:
        model = PlaygroundAnomalyDetectionExample
        fields = ['name', 'capability']