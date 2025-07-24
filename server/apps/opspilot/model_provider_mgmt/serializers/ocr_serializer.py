from apps.core.utils.serializers import AuthSerializer
from apps.opspilot.models import OCRProvider


class OCRProviderSerializer(AuthSerializer):
    permission_key = "provider.orc_model"

    class Meta:
        model = OCRProvider
        fields = "__all__"
