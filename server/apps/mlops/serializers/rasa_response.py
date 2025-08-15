from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_response import RasaResponse

class RasaResponseSerializer(AuthSerializer):
    permission_key = "dataset.rasa_response"

    class Meta:
        model = RasaResponse
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'example': {'required': False},
            'dataset': {'required': False},
        }