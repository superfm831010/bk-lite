from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.anomaly_detection_dataset import AnomalyDetectionDataset


class AnomalyDetectionDatasetSerializer(AuthSerializer):
    """异常检测数据集序列化器"""
    permission_key = "dataset.anomaly_detection_dataset"
    
    class Meta:
        model = AnomalyDetectionDataset
        fields = "__all__"
