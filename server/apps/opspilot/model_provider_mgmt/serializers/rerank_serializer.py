from apps.core.utils.serializers import AuthSerializer
from apps.opspilot.models import RerankProvider


class RerankProviderSerializer(AuthSerializer):
    permission_key = "provider.rerank_model"

    class Meta:
        model = RerankProvider
        fields = "__all__"
