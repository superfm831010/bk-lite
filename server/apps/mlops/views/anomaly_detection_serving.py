
from config.drf.viewsets import ModelViewSet
from apps.core.decorators.api_permission import HasPermission
from apps.mlops.algorithm.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector
from apps.mlops.filters.anomaly_detection_serving import AnomalyDetectionServingFilter
from apps.mlops.models.anomaly_detection_serving import AnomalyDetectionServing
from apps.mlops.serializers.anomaly_detection_serving import AnomalyDetectionServingSerializer
from config.drf.pagination import CustomPageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
import pandas as pd


class AnomalyDetectionServingViewSet(ModelViewSet):
    queryset = AnomalyDetectionServing.objects.all()
    serializer_class = AnomalyDetectionServingSerializer
    filterset_class = AnomalyDetectionServingFilter
    pagination_class = CustomPageNumberPagination
    permission_key = "serving.anomaly_detection_serving"

    @HasPermission("model_release-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("model_release-Add,train_tasks-View")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("model_release-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission("model_release-Update")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @HasPermission("model_release-View")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @HasPermission("model_release-View")
    @action(detail=False, methods=['post'], url_path='predict')
    def predict(self, request, pk=None):
        """
        异常检测推理接口

        通过AnomalyDetectionServing的id获取模型配置，接收JSON数据进行异常检测推理
        """
        try:
            # 获取并验证请求数据
            data = request.data
            serving_id = data.get('serving_id')
            time_series_data = data.get('data')

            # 验证必需参数
            if not serving_id:
                return Response(
                    {'error': 'serving_id参数是必需的'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not time_series_data:
                return Response(
                    {'error': 'data参数是必需的'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 获取异常检测服务配置
            try:
                serving = AnomalyDetectionServing.objects.select_related(
                    'anomaly_detection_train_job').get(id=serving_id)
            except AnomalyDetectionServing.DoesNotExist:
                return Response(
                    {'error': f'异常检测服务不存在: {serving_id}'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 检查服务状态是否启用
            if serving.status != 'active':
                return Response(
                    {'error': f'异常检测服务未启用，当前状态: {serving.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 检查关联的训练任务状态
            train_job = serving.anomaly_detection_train_job
            if train_job.status != 'completed':
                return Response(
                    {'error': f'关联的训练任务未完成，当前状态: {train_job.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 从服务配置和训练任务获取模型信息
            model_name = f"{train_job.algorithm}_{train_job.id}"  # 基于训练任务ID生成模型名称
            model_version = serving.model_version
            anomaly_threshold = serving.anomaly_threshold
            algorithm = train_job.algorithm

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
                'serving_id': serving_id,
                'serving_name': serving.name,
                'train_job_id': train_job.id,
                'train_job_name': train_job.name,
                'algorithm': algorithm,
                'model_name': model_name,
                'model_version': model_version,
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
