from django_filters import rest_framework as filters
from apps.log.models.collect_config import CollectType, CollectInstance, CollectConfig


class CollectTypeFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    collector = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CollectType
        fields = ['name', 'collector']


class CollectInstanceFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    collect_type = filters.CharFilter(field_name='collect_type__name', lookup_expr='icontains')

    class Meta:
        model = CollectInstance
        fields = ['name', 'collect_type']


class CollectConfigFilter(filters.FilterSet):
    collect_instance = filters.CharFilter(field_name='collect_instance__name', lookup_expr='icontains')
    file_type = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CollectConfig
        fields = ['collect_instance', 'file_type']