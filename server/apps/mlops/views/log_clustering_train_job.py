from config.drf.viewsets import ModelViewSet
from apps.mlops.filters.log_clustering_train_job import LogClusteringTrainJobFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.core.logger import opspilot_logger as logger
from apps.core.decorators.api_permission import HasPermission
from apps.mlops.models.log_clustering_train_job import LogClusteringTrainJob
from apps.mlops.serializers.log_clustering_train_job import LogClusteringTrainJobSerializer
from config.drf.pagination import CustomPageNumberPagination


class LogClusteringTrainJobViewSet(ModelViewSet):
    queryset = LogClusteringTrainJob.objects.all()
    serializer_class = LogClusteringTrainJobSerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = LogClusteringTrainJobFilter
    ordering = ("-id",)
    permission_key = "dataset.log_clustering_train_job"

    @HasPermission("log_clustering_train_jobs-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("log_clustering_train_jobs-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @HasPermission("log_clustering_train_jobs-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("log_clustering_train_jobs-Add")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("log_clustering_train_jobs-Edit")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)