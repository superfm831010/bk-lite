from apps.core.utils.serializers import AuthSerializer
from rest_framework import serializers
from apps.mlops.models.rasa_form import RasaForm


class RasaFormSerializer(AuthSerializer):

    permission_key = "dataset.rasa_form"

    slot_count = serializers.SerializerMethodField(read_only=True,help_text="意图示例数量")

    class Meta:
        model = RasaForm
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'slots': {'required': False},
            'dataset': {'required': False},
        }

    def get_slot_count(self, obj):
        if isinstance(obj.slots, list):
            return len(obj.slots)
        return 0