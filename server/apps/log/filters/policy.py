import django_filters
from apps.log.models.policy import Policy, Alert, Event


class PolicyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    alert_type = django_filters.CharFilter(lookup_expr='exact')
    alert_level = django_filters.CharFilter(lookup_expr='exact')
    collect_type = django_filters.NumberFilter(field_name='collect_type__id')
    notice = django_filters.BooleanFilter()
    created_by = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Policy
        fields = ['name', 'alert_type', 'alert_level', 'collect_type', 'notice', 'created_by', 'created_at']


class AlertFilter(django_filters.FilterSet):
    policy = django_filters.NumberFilter(field_name='policy__id')
    policy_name = django_filters.CharFilter(field_name='policy__name', lookup_expr='icontains')
    collect_type = django_filters.NumberFilter(field_name='collect_type__id')
    level = django_filters.CharFilter(lookup_expr='exact')
    status = django_filters.CharFilter(lookup_expr='exact')
    source_id = django_filters.CharFilter(lookup_expr='icontains')
    start_event_time = django_filters.DateTimeFromToRangeFilter()
    end_event_time = django_filters.DateTimeFromToRangeFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Alert
        fields = ['policy', 'policy_name', 'collect_type', 'level', 'status', 'source_id',
                 'start_event_time', 'end_event_time', 'created_at']


class EventFilter(django_filters.FilterSet):
    policy = django_filters.NumberFilter(field_name='policy__id')
    alert = django_filters.CharFilter(field_name='alert__id')
    source_id = django_filters.CharFilter(lookup_expr='icontains')
    level = django_filters.CharFilter(lookup_expr='exact')
    event_time = django_filters.DateTimeFromToRangeFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Event
        fields = ['policy', 'alert', 'source_id', 'level', 'event_time', 'created_at']
