from apps.core.utils.viewset_utils import AuthViewSet
from apps.opspilot.model_provider_mgmt.serializers.embed_serializer import EmbedProviderSerializer
from apps.opspilot.models import EmbedProvider


class EmbedProviderViewSet(AuthViewSet):
    serializer_class = EmbedProviderSerializer
    queryset = EmbedProvider.objects.all()
    search_fields = ["name"]
    permission_key = "provider.embed_model"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.query_by_groups(request, queryset)
