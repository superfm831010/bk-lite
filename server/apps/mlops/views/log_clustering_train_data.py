from config.drf.viewsets import ModelViewSet
from apps.mlops.filters.log_clustering_train_data import LogClusteringTrainDataFilter
from rest_framework import viewsets

from apps.core.logger import opspilot_logger as logger
from apps.core.decorators.api_permission import HasPermission
from apps.mlops.models.log_clustering_train_data import LogClusteringTrainData
from apps.mlops.serializers.log_clustering_train_data import LogClusteringTrainDataSerializer
from config.drf.pagination import CustomPageNumberPagination


class LogClusteringTrainDataViewSet(ModelViewSet):
    queryset = LogClusteringTrainData.objects.all()
    serializer_class = LogClusteringTrainDataSerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = LogClusteringTrainDataFilter
    ordering = ("-id",)
    permission_key = "dataset.log_clustering_train_data"

    @HasPermission("log_clustering_train_data-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("log_clustering_train_data-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @HasPermission("log_clustering_train_data-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("log_clustering_train_data-Add")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("log_clustering_train_data-Edit")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)