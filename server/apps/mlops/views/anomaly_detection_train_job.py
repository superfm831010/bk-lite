from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
import pandas as pd

import mlflow
from config.components.mlflow import MLFLOW_TRACKER_URL
from apps.core.decorators.api_permission import HasPermission
from config.drf.viewsets import ModelViewSet
from apps.mlops.filters.anomaly_detection_dataset import AnomalyDetectionDatasetFilter
from apps.mlops.filters.anomaly_detection_train_job import AnomalyDetectionTrainJobFilter
from apps.mlops.models.anomaly_detection_train_job import AnomalyDetectionTrainJob
from apps.mlops.models.anomaly_detection_serving import AnomalyDetectionServing
from apps.mlops.serializers.anomaly_detection_train_job import AnomalyDetectionTrainJobSerializer
from apps.mlops.tasks.anomaly_detection_train_task import start_anomaly_detection_train
from apps.mlops.algorithm.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector
from config.drf.pagination import CustomPageNumberPagination


class AnomalyDetectionTrainJobViewSet(ModelViewSet):
   queryset= AnomalyDetectionTrainJob.objects.all()
   serializer_class = AnomalyDetectionTrainJobSerializer
   filterset_class = AnomalyDetectionTrainJobFilter
   pagination_class=CustomPageNumberPagination
   permission_key = "dataset.anomaly_detection_train_job"

   @action(detail=True, methods=['post'], url_path='train')
   @HasPermission("train_tasks-Train")
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

   @action(detail=True, methods=['get'], url_path='metrics-history')
   @HasPermission("train_tasks-View")
   def get_metrics_history(self, request, pk=None):
      """
      获取指定训练任务的指标历史数据，用于绘制图表
      """
      try:
         # 获取训练任务
         train_job = self.get_object()

         # 设置MLflow跟踪URI
         mlflow.set_tracking_uri(MLFLOW_TRACKER_URL)

         # 构造实验名称（与训练时保持一致）
         experiment_name = f"{train_job.id}_{train_job.name}"

         # 查找实验
         experiments = mlflow.search_experiments(filter_string=f"name = '{experiment_name}'")
         if not experiments:
            return Response(
               {'error': '未找到对应的MLflow实验'},
               status=status.HTTP_404_NOT_FOUND
            )

         experiment = experiments[0]

         # 查找该实验中的运行
         runs = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"],
         )

         if runs.empty:
            return Response(
               {'error': '未找到训练运行记录'},
               status=status.HTTP_404_NOT_FOUND
            )

         # 获取所有的run_id
         run_ids = runs["run_id"].tolist()
         #每次运行信息的耗时和名称
         run_datas = []
         for _,row in runs.iterrows():
            duration = row["end_time"] - row["start_time"]
            duration_minutes = duration.total_seconds() / 60
            run_data = {
               "run_id": row["run_id"],
               "duration": duration_minutes,
               "run_name": row["tags.mlflow.runName"]
            }
            run_datas.append(run_data)
         # 创建MLflow客户端
         client = mlflow.tracking.MlflowClient()

         # 定义需要获取历史的指标
         important_metrics = [metric for metric in client.get_run(run_ids[0]).data.metrics.keys() if not str(metric).startswith("system")]

         data = []
         for run_data in run_datas:
            # 获取每个指标的历史数据
            metrics_history = {}
            run_id = run_data["run_id"]
            for metric_name in important_metrics:
               try:
                  # 获取指标历史数据
                  history = client.get_metric_history(run_id, metric_name)
                  metrics_history[metric_name] = [
                     {
                        "step": metric.step,
                        "value": metric.value
                     }
                     for metric in history
                  ]
               except Exception:
                  # 如果获取历史失败，跳过该指标
                  pass
            run_data["metrics_history"] = metrics_history
            data.append(run_data)

         return Response({
            'train_job_id': train_job.id,
            'train_job_name': train_job.name,
            'data': data
         })

      except Exception as e:
         return Response(
            {'error': f'获取指标历史失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )

   @HasPermission("train_tasks-View")
   def list(self, request, *args, **kwargs):
      return super().list(request, *args, **kwargs)

   @HasPermission("train_tasks-Add,anomaly_detection_datasets_detail-File View,anomaly_detection_datasets-View")
   def create(self, request, *args, **kwargs):
      return super().create(request, *args, **kwargs)

   @HasPermission("train_tasks-Delete")
   def destroy(self, request, *args, **kwargs):
      return super().destroy(request, *args, **kwargs)

   @HasPermission("train_tasks-Edit")
   def update(self, request, *args, **kwargs):
      return super().update(request, *args, **kwargs)

   @HasPermission("train_tasks-View")
   def retrieve(self, request, *args, **kwargs):
      return super().retrieve(request, *args, **kwargs)