from config.drf.viewsets import ModelViewSet
from apps.mlops.filters.log_clustering_dataset import LogClusteringDatasetFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.core.logger import opspilot_logger as logger
from apps.core.decorators.api_permission import HasPermission
from apps.mlops.models.log_clustering_dataset import LogClusteringDataset
from apps.mlops.serializers.log_clustering_dataset import LogClusteringDatasetSerializer
from config.drf.pagination import CustomPageNumberPagination


class LogClusteringDatasetViewSet(ModelViewSet):
    queryset = LogClusteringDataset.objects.all()
    serializer_class = LogClusteringDatasetSerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = LogClusteringDatasetFilter
    ordering = ("-id",)
    permission_key = "dataset.log_clustering_dataset"

    @HasPermission("log_clustering_datasets-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("log_clustering_datasets-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @HasPermission("log_clustering_datasets-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("log_clustering_datasets-Add")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("log_clustering_datasets-Edit")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)