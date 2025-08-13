from apps.core.utils.serializers import AuthSerializer
from apps.opspilot.model_provider_mgmt.serializers.model_type_serializer import ModelTypeSerializer
from apps.opspilot.models import OCRProvider


class OCRProviderSerializer(AuthSerializer, ModelTypeSerializer):
    permission_key = "provider.orc_model"

    class Meta:
        model = OCRProvider
        fields = "__all__"
