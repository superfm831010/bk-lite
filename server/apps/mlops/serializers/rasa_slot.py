from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_slot import RasaSlot

class RasaSlotSerializer(AuthSerializer):
    permission_key = "dataset.rasa_slot"

    class Meta:
        model = RasaSlot
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'dataset': {'required': False},
            'values': {'required': False},
        }