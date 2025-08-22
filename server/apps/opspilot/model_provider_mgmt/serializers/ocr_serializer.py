from apps.core.utils.serializers import AuthSerializer
from apps.opspilot.model_provider_mgmt.serializers.model_type_serializer import ProviderModelTypeSerializer
from apps.opspilot.models import OCRProvider


class OCRProviderSerializer(AuthSerializer, ProviderModelTypeSerializer):
    permission_key = "provider.ocr_model"

    class Meta:
        model = OCRProvider
        fields = "__all__"
