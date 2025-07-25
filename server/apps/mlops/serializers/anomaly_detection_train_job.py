from apps.mlops.models.anomaly_detection_train_job import AnomalyDetectionTrainJob
from apps.core.utils.serializers import AuthSerializer


class AnomalyDetectionTrainJobSerializer(AuthSerializer):
    permission_key = "dataset.anomaly_detection_train_job"
    
    class Meta:
        model = AnomalyDetectionTrainJob
        fields = "__all__"