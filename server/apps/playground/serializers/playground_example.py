from apps.core.utils.serializers import AuthSerializer
from rest_framework import serializers
from apps.playground.models.playground_example import PlayGroundFile
from apps.mlops.models.anomaly_detection_serving import AnomalyDetectionServing

class PlayGroundFileSerializer(AuthSerializer):
    permission_key = 'playground.playground_example'
    serving = serializers.PrimaryKeyRelatedField(
        queryset=AnomalyDetectionServing.objects.all(),
        required=True,
    )

    class Meta:
        model = PlayGroundFile
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'train_data': {'required': False},
            'serving': {'required': True},
            'is_active': {'required': False},
        }

    def get_serving(self, obj):
        from apps.mlops.serializers.anomaly_detection_serving import AnomalyDetectionServingSerializer
        return AnomalyDetectionServingSerializer(obj.serving).data if obj.serving else None

    def to_representation(self, instance):
        from apps.mlops.serializers.anomaly_detection_serving import AnomalyDetectionServingSerializer
        ret = super().to_representation(instance)
        ret['serving_id'] = AnomalyDetectionServingSerializer(instance.serving, context=self.context).data
        return ret