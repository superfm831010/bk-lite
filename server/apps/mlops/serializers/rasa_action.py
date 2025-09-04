from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_action import RasaAction
from rest_framework import serializers

class RasaActionSerializer(AuthSerializer):
    permission_key = "dataset.rasa_action"

    example_count = serializers.SerializerMethodField(read_only=True, help_text="Action数量")

    class Meta:
        model = RasaAction
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'dataset': {'required': False},
        }
