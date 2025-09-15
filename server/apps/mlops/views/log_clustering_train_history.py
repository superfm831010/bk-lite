from config.drf.viewsets import ModelViewSet
from apps.mlops.filters.log_clustering_train_history import LogClusteringTrainHistoryFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.core.logger import opspilot_logger as logger
from apps.core.decorators.api_permission import HasPermission
from apps.mlops.models.log_clustering_train_history import LogClusteringTrainHistory
from apps.mlops.serializers.log_clustering_train_history import LogClusteringTrainHistorySerializer
from config.drf.pagination import CustomPageNumberPagination


class LogClusteringTrainHistoryViewSet(ModelViewSet):
    queryset = LogClusteringTrainHistory.objects.all()
    serializer_class = LogClusteringTrainHistorySerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = LogClusteringTrainHistoryFilter
    ordering = ("-id",)
    permission_key = "dataset.log_clustering_train_history"

    @HasPermission("log_clustering_train_history-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("log_clustering_train_history-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @HasPermission("log_clustering_train_history-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("log_clustering_train_history-Add")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("log_clustering_train_history-Edit")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)