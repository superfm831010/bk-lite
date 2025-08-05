from apps.core.utils.serializers import AuthSerializer
from rest_framework import serializers
from apps.playground.models.playground_example import PlayGroundFile
from apps.playground.models.playground_capability import PlayGroundCapability

class PlayGroundFileSerializer(AuthSerializer):
    permission_key = 'playground.playground_example'
    capability = serializers.PrimaryKeyRelatedField(
        queryset=PlayGroundCapability.objects.all(),
        required=True,
    )

    class Meta:
        model = PlayGroundFile
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'train_data': {'required': False},
            'capability': {'required': True},
            'is_active': {'required': False},
        }

    def get_capability(self, obj):
        from apps.playground.serializers.playground_capability import PlayGroundCapabilitySerializer
        return PlayGroundCapabilitySerializer(obj.capability).data if obj.capability else None

    def to_representation(self, instance):
        from apps.playground.serializers.playground_capability import PlayGroundCapabilitySerializer
        ret = super().to_representation(instance)
        ret['capability'] = PlayGroundCapabilitySerializer(instance.capability, context=self.context).data
        return ret