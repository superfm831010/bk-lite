from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_intent import RasaIntent

class RasaIntentSerializer(AuthSerializer):
    permission_key = "dataset.rasa_intent"

    class Meta:
        model = RasaIntent
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'example': {'required': False},
            'dataset': {'required': False},
        }

