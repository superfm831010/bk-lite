from config.drf.viewsets import ModelViewSet
from apps.mlops.filters.anomaly_detection_dataset import AnomalyDetectionDatasetFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.core.logger import opspilot_logger as logger
from apps.core.decorators.api_permission import HasPermission
from apps.mlops.models.anomaly_detection_dataset import AnomalyDetectionDataset
from apps.mlops.serializers.anomaly_detection_dataset import AnomalyDetectionDatasetSerializer
from config.drf.pagination import CustomPageNumberPagination


class AnomalyDetectionDatasetViewSet(ModelViewSet):
    queryset = AnomalyDetectionDataset.objects.all()
    serializer_class = AnomalyDetectionDatasetSerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = AnomalyDetectionDatasetFilter
    ordering = ("-id",)
    permission_key = "dataset.anomaly_detection_dataset"

    @HasPermission("anomaly_detection_datasets-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets-Add")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets-Edit")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)