from apps.core.utils.serializers import AuthSerializer
from apps.opspilot.model_provider_mgmt.serializers.model_type_serializer import CustomProviderSerializer
from apps.opspilot.models import EmbedProvider


class EmbedProviderSerializer(AuthSerializer, CustomProviderSerializer):
    permission_key = "provider.embed_model"

    class Meta:
        model = EmbedProvider
        fields = "__all__"
