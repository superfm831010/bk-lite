from apps.core.utils.serializers import AuthSerializer
from apps.opspilot.model_provider_mgmt.serializers.model_type_serializer import ModelTypeSerializer
from apps.opspilot.models import RerankProvider


class RerankProviderSerializer(AuthSerializer, ModelTypeSerializer):
    permission_key = "provider.rerank_model"

    class Meta:
        model = RerankProvider
        fields = "__all__"
