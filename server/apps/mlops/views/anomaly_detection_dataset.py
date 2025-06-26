from apps.core.utils.viewset_utils import AuthViewSet
from apps.mlops.filters.anomaly_detection_dataset import AnomalyDetectionDatasetFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.core.logger import opspilot_logger as logger
from apps.mlops.models.anomaly_detection_dataset import AnomalyDetectionDataset
from apps.mlops.serializers.anomaly_detection_dataset import AnomalyDetectionDatasetSerializer
from config.drf.pagination import CustomPageNumberPagination


class AnomalyDetectionDatasetViewSet(AuthViewSet):
    queryset = AnomalyDetectionDataset.objects.all()
    serializer_class = AnomalyDetectionDatasetSerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = AnomalyDetectionDatasetFilter
    ordering = ("-id",)
    permission_key = "dataset.anomaly_detection_dataset"
