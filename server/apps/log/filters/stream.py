from django_filters import rest_framework as filters
from apps.log.models.stream import Stream

class StreamFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    rule = filters.CharFilter(field_name="rule", lookup_expr="icontains")
    collect_type_id = filters.NumberFilter(field_name="collect_type__id")

    class Meta:
        model = Stream
        fields = ["name", "rule", "collect_type_id"]