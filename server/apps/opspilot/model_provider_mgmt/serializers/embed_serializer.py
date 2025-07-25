from apps.core.utils.serializers import AuthSerializer
from apps.opspilot.models import EmbedProvider


class EmbedProviderSerializer(AuthSerializer):
    permission_key = "provider.embed_model"

    class Meta:
        model = EmbedProvider
        fields = "__all__"
