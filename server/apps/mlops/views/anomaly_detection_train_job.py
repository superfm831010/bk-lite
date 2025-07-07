from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
import pandas as pd

from apps.core.utils.viewset_utils import AuthViewSet
from apps.mlops.filters.anomaly_detection_dataset import AnomalyDetectionDatasetFilter
from apps.mlops.filters.anomaly_detection_train_job import AnomalyDetectionTrainJobFilter
from apps.mlops.models.anomaly_detection_train_job import AnomalyDetectionTrainJob
from apps.mlops.models.anomaly_detection_serving import AnomalyDetectionServing
from apps.mlops.serializers.anomaly_detection_train_job import AnomalyDetectionTrainJobSerializer
from apps.mlops.tasks.anomaly_detection_train_task import start_anomaly_detection_train
from apps.mlops.algorithm.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector
from config.drf.pagination import CustomPageNumberPagination


class AnomalyDetectionTrainJobViewSet(AuthViewSet):
   queryset= AnomalyDetectionTrainJob.objects.all()
   serializer_class = AnomalyDetectionTrainJobSerializer
   filterset_class = AnomalyDetectionTrainJobFilter
   pagination_class=CustomPageNumberPagination
   permission_key = "dataset.anomaly_detection_train_job"

      
   @action(detail=True, methods=['post'], url_path='train')
   def train(self, request, pk=None):
      try:
         train_job = self.get_object()
         start_anomaly_detection_train.delay(train_job.id)

         return Response(
            status=status.HTTP_200_OK
         )
         
      except ValueError as e:
         return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
         )
      except Exception as e:
         return Response(
            {'error': f'训练启动失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )