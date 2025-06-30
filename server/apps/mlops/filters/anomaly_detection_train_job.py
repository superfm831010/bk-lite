from apps.mlops.models.anomaly_detection_train_job import AnomalyDetectionTrainJob
from django_filters.rest_framework import FilterSet


class AnomalyDetectionTrainJobFilter(FilterSet):
    class Meta:
        model = AnomalyDetectionTrainJob
        fields = {
            "name": ["exact", "icontains"],
            "status": ["exact"],
            "algorithm": ["exact"],
        }
