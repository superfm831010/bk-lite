from apps.core.utils.viewset_utils import AuthViewSet
from apps.opspilot.model_provider_mgmt.serializers.rerank_serializer import RerankProviderSerializer
from apps.opspilot.models import RerankProvider


class RerankProviderViewSet(AuthViewSet):
    queryset = RerankProvider.objects.all()
    serializer_class = RerankProviderSerializer
    permission_key = "provider.rerank_model"
