from config.drf.viewsets import ModelViewSet
from apps.mlops.filters.log_clustering_serving import LogClusteringServingFilter
from rest_framework import viewsets

from apps.core.logger import opspilot_logger as logger
from apps.core.decorators.api_permission import HasPermission
from apps.mlops.models.log_clustering_serving import LogClusteringServing
from apps.mlops.serializers.log_clustering_serving import LogClusteringServingSerializer
from config.drf.pagination import CustomPageNumberPagination


class LogClusteringServingViewSet(ModelViewSet):
    queryset = LogClusteringServing.objects.all()
    serializer_class = LogClusteringServingSerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = LogClusteringServingFilter
    ordering = ("-id",)
    permission_key = "dataset.log_clustering_serving"

    @HasPermission("log_clustering_servings-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("log_clustering_servings-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @HasPermission("log_clustering_servings-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("log_clustering_servings-Add")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("log_clustering_servings-Edit")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)