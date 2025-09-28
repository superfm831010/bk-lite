from config.drf.viewsets import ModelViewSet
from apps.mlops.filters.timeseries_predict_train_history import TimeSeriesPredictTrainHistoryFilter
from rest_framework import viewsets

from apps.core.logger import opspilot_logger as logger
from apps.core.decorators.api_permission import HasPermission
from apps.mlops.models.timeseries_predict_train_history import TimeSeriesPredictTrainHistory
from apps.mlops.serializers.timeseries_predict_train_history import TimeSeriesPredictTrainHistorySerializer
from config.drf.pagination import CustomPageNumberPagination


class TimeSeriesPredictTrainHistoryViewSet(ModelViewSet):
    queryset = TimeSeriesPredictTrainHistory.objects.all()
    serializer_class = TimeSeriesPredictTrainHistorySerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = TimeSeriesPredictTrainHistoryFilter
    ordering = ("-id",)
    permission_key = "dataset.timeseries_predict_train_history"

    @HasPermission("timeseries_predict_train_history-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("timeseries_predict_train_history-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @HasPermission("timeseries_predict_train_history-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("timeseries_predict_train_history-Add")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("timeseries_predict_train_history-Edit")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)