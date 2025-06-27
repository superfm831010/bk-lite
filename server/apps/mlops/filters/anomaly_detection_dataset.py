from apps.mlops.models.anomaly_detection_dataset import AnomalyDetectionDataset
from django_filters import filters
from django_filters.rest_framework import FilterSet


class AnomalyDetectionDatasetFilter(FilterSet):
    """异常检测数据集过滤器"""

    class Meta:
        model = AnomalyDetectionDataset
        fields = {
            "name": ["exact", "icontains"],
        }
