from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
import pandas as pd

from apps.core.utils.viewset_utils import AuthViewSet
from apps.mlops.filters.anomaly_detection_dataset import AnomalyDetectionDatasetFilter
from apps.mlops.filters.anomaly_detection_train_job import AnomalyDetectionTrainJobFilter
from apps.mlops.models.anomaly_detection_train_job import AnomalyDetectionTrainJob
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

   @action(detail=False, methods=['post'], url_path='predict')
   def predict(self, request, pk=None):
      """
      异常检测推理接口
      
      接收JSON数据进行异常检测推理，返回异常概率和异常判断结果
      """
      try:
         # 获取并验证请求数据
         data = request.data
         model_name = data.get('model_name')
         model_version = data.get('model_version', 'latest')
         algorithm = data.get('algorithm')
         time_series_data = data.get('data')
         anomaly_threshold = data.get('anomaly_threshold', 0.5)
         
         # 将数据转换为DataFrame
         df = pd.DataFrame(time_series_data)
         
         # 根据算法类型选择对应的检测器
         if algorithm == 'RandomForest':
            detector = RandomForestAnomalyDetector()
         else:
            return Response(
               {'error': f'不支持的算法类型: {algorithm}'},
               status=status.HTTP_400_BAD_REQUEST
            )
         
         # 执行异常检测推理
         result_df = detector.predict(df, model_name, model_version)
         
         # 根据阈值判断异常点
         result_df['is_anomaly'] = (result_df['anomaly_probability'] >= anomaly_threshold).astype(int)
         
         # 构造返回结果
         predictions = []
         for idx, (i, row) in enumerate(result_df.iterrows()):
            predictions.append({
               'timestamp': time_series_data[idx]['timestamp'],
               'value': float(row['value']),
               'anomaly_probability': float(row['anomaly_probability']),
               'is_anomaly': int(row['is_anomaly'])
            })
         
         return Response({
            'success': True,
            'model_name': model_name,
            'model_version': model_version,
            'algorithm': algorithm,
            'anomaly_threshold': anomaly_threshold,
            'total_points': len(predictions),
            'anomaly_count': sum(p['is_anomaly'] for p in predictions),
            'predictions': predictions
         }, status=status.HTTP_200_OK)
         
      except Exception as e:
         return Response(
            {'error': f'推理失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )
      
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