from apps.core.utils.serializers import AuthSerializer
from rest_framework import serializers
from apps.playground.models.playground_example import PlaygroundAnomalyDetectionExample

class PlaygroundAnomalyDetectionExampleSerializer(AuthSerializer):
    permission_key = 'playground.playground_example'

    class Meta:
        model = PlaygroundAnomalyDetectionExample
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'train_data': {'required': False},
            'capability': {'required': True},
            'is_active': {'required': False},
        }
