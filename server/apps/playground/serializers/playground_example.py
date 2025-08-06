from apps.core.utils.serializers import AuthSerializer
from rest_framework import serializers
from apps.playground.models.playground_example import PlayGroundFile

class PlayGroundFileSerializer(AuthSerializer):
    permission_key = 'playground.playground_example'

    class Meta:
        model = PlayGroundFile
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'train_data': {'required': False},
            'serving': {'required': True},
            'is_active': {'required': False},
        }
