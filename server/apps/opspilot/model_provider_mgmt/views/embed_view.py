from django_filters import filters
from django_filters.rest_framework import FilterSet

from apps.core.utils.viewset_utils import AuthViewSet
from apps.opspilot.model_provider_mgmt.serializers.embed_serializer import EmbedProviderSerializer
from apps.opspilot.models import EmbedProvider


class ObjFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    enabled = filters.CharFilter(method="filter_enabled")

    @staticmethod
    def filter_enabled(qs, field_name, value):
        """查询类型"""
        if not value:
            return qs
        enabled = value == "1"
        return qs.filter(enabled=enabled)


class EmbedProviderViewSet(AuthViewSet):
    serializer_class = EmbedProviderSerializer
    queryset = EmbedProvider.objects.all()
    permission_key = "provider.embed_model"
    filterset_class = ObjFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.query_by_groups(request, queryset)
