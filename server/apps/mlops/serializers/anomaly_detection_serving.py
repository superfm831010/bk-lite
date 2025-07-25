from apps.core.utils.serializers import AuthSerializer
from rest_framework import serializers
from apps.mlops.models.anomaly_detection_serving import AnomalyDetectionServing


class AnomalyDetectionServingSerializer(AuthSerializer):

    permission_key = "serving.anomaly_detection_serving"

    class Meta:
        model = AnomalyDetectionServing
        fields = "__all__"
