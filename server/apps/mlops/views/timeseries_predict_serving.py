from config.drf.viewsets import ModelViewSet
from apps.mlops.filters.timeseries_predict_serving import TimeSeriesPredictServingFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.core.logger import opspilot_logger as logger
from apps.core.decorators.api_permission import HasPermission
from apps.mlops.models.timeseries_predict_serving import TimeSeriesPredictServing
from apps.mlops.serializers.timeseries_predict_serving import TimeSeriesPredictServingSerializer
from config.drf.pagination import CustomPageNumberPagination


class TimeSeriesPredictServingViewSet(ModelViewSet):
    queryset = TimeSeriesPredictServing.objects.all()
    serializer_class = TimeSeriesPredictServingSerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = TimeSeriesPredictServingFilter
    ordering = ("-id",)
    permission_key = "dataset.timeseries_predict_serving"

    @HasPermission("timeseries_predict_servings-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("timeseries_predict_servings-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @HasPermission("timeseries_predict_servings-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("timeseries_predict_servings-Add")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("timeseries_predict_servings-Edit")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)