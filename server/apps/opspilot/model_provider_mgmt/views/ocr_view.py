from django_filters import filters
from django_filters.rest_framework import FilterSet

from apps.core.utils.viewset_utils import AuthViewSet
from apps.opspilot.model_provider_mgmt.serializers.ocr_serializer import OCRProviderSerializer
from apps.opspilot.models import OCRProvider


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


class OCRProviderViewSet(AuthViewSet):
    queryset = OCRProvider.objects.all()
    serializer_class = OCRProviderSerializer
    permission_key = "provider.orc_model"
    filterset_class = ObjFilter
