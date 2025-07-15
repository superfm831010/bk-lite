from apps.mlops.models.anomaly_detection_serving import AnomalyDetectionServing
from django_filters.rest_framework import FilterSet

class AnomalyDetectionServingFilter(FilterSet):
    """异常检测服务过滤器"""

    class Meta:
        model = AnomalyDetectionServing
        fields = {
            "name": ["exact", "icontains"],
            "anomaly_detection_train_job": ["exact"],
            "status": ["exact"],
        }