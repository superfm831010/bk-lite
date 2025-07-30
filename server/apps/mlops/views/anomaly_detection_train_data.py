import csv
import json
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from apps.core.decorators.api_permission import HasPermission
from apps.core.utils.viewset_utils import AuthViewSet, MaintainerViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from apps.mlops.filters.anomaly_detection_train_data import AnomalyDetectionTrainDataFilter
from apps.mlops.models.anomaly_detection_train_data import AnomalyDetectionTrainData
from apps.mlops.serializers.anomaly_detection_train_data import AnomalyDetectionTrainDataSerializer
from config.drf.pagination import CustomPageNumberPagination
import pandas as pd


class AnomalyDetectionTrainDataViewSet(AuthViewSet):
    """异常检测训练数据视图集"""
    
    queryset = AnomalyDetectionTrainData.objects.all()
    serializer_class = AnomalyDetectionTrainDataSerializer
    filterset_class = AnomalyDetectionTrainDataFilter
    pagination_class = CustomPageNumberPagination
    permission_key = "dataset.anomaly_detection_train_data"

    @HasPermission("anomaly_detection_datasets-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets-File Upload")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets-File Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets-File Edit,anomaly_detection_datasets-File Tag")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)