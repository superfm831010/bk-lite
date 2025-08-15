import csv
import json
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from apps.core.decorators.api_permission import HasPermission
from config.drf.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from apps.mlops.filters.anomaly_detection_train_data import AnomalyDetectionTrainDataFilter
from apps.mlops.models.anomaly_detection_train_data import AnomalyDetectionTrainData
from apps.mlops.serializers.anomaly_detection_train_data import AnomalyDetectionTrainDataSerializer
from config.drf.pagination import CustomPageNumberPagination
import pandas as pd


class AnomalyDetectionTrainDataViewSet(ModelViewSet):
    """异常检测训练数据视图集"""
    
    queryset = AnomalyDetectionTrainData.objects.all()
    serializer_class = AnomalyDetectionTrainDataSerializer
    filterset_class = AnomalyDetectionTrainDataFilter
    pagination_class = CustomPageNumberPagination
    permission_key = "dataset.anomaly_detection_train_data"

    @HasPermission("anomaly_detection_datasets_detail-File View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets_detail-File Upload")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets_detail-File Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets_detail-File Edit")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @HasPermission("anomaly_detection_datasets_detail-File View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)