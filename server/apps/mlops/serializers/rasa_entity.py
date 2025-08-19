from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_entity import RasaEntity

class RasaEntitySerializer(AuthSerializer):
    permission_key = "dataset.rasa_entity"
    class Meta:
        model = RasaEntity
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'example': {'required': False},
            'dataset': {'required': False},
        }