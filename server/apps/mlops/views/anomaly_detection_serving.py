
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
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


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
            
            # 确保DataFrame有timestamp列，以便后续能够正确映射回原始数据
            if 'timestamp' not in df.columns and len(time_series_data) > 0:
                # 如果没有timestamp列，添加索引作为timestamp
                df['timestamp'] = [item.get('timestamp', f'index_{i}') for i, item in enumerate(time_series_data)]

            # 调试：检查数据转换后的状态
            logger.info(f"数据预处理前调试信息:")
            logger.info(f"  - 原始数据长度: {len(time_series_data)}")
            logger.info(f"  - DataFrame形状: {df.shape}")
            logger.info(f"  - DataFrame列: {df.columns.tolist()}")
            logger.info(f"  - DataFrame前5行: {df.head().to_dict('records')}")
            logger.info(f"  - DataFrame后5行: {df.tail().to_dict('records')}")

            # 根据算法类型选择对应的检测器
            if algorithm == 'RandomForest':
                detector = RandomForestAnomalyDetector()
            else:
                return Response(
                    {'error': f'不支持的算法类型: {algorithm}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 执行异常检测推理
            # 使用改进的预测方法，避免频率重采样导致的数据扩展问题
            try:
                # 首先尝试使用不重采样的方法
                model = detector._load_model_with_cache(model_name, model_version)
                result_df = detector._predict_without_resampling(df, model)
                logger.info(f"使用无重采样方法成功，结果长度: {len(result_df)}")
            except Exception as e:
                logger.warning(f"无重采样方法失败: {str(e)}，回退到标准方法")
                # 回退到原始方法
                result_df = detector.predict(df, model_name, model_version)
            
            # 添加调试信息
            logger.info(f"异常检测推理调试信息:")
            logger.info(f"  - 原始数据长度: {len(time_series_data)}")
            logger.info(f"  - 输入DataFrame形状: {df.shape}")
            logger.info(f"  - 结果DataFrame形状: {result_df.shape}")
            logger.info(f"  - 结果DataFrame列: {result_df.columns.tolist()}")
            
            # 确保result_df的长度不超过原始数据长度，并处理长度不匹配的情况
            if len(result_df) != len(time_series_data):
                logger.warning(f"结果长度 ({len(result_df)}) != 原始长度 ({len(time_series_data)})")
                
                if len(result_df) > len(time_series_data):
                    # 如果结果比原始数据长，截断到原始长度
                    logger.info("截断结果到原始数据长度")
                    result_df = result_df.head(len(time_series_data))
                elif len(result_df) < len(time_series_data):
                    # 如果结果比原始数据短，可能是由于dropna()造成的
                    # 为了保持数据对齐，我们需要重新索引
                    logger.warning("结果数据少于原始数据，可能由于数据清理造成")
                    # 这种情况下我们需要特殊处理索引对应关系
                    # 在后续的predictions构造中会处理这个问题
            
            # 根据阈值判断异常点
            result_df['is_anomaly'] = (result_df['anomaly_probability'] >= anomaly_threshold).astype(int)

            # 构造返回结果
            predictions = []
            
            # 处理结果长度与原始数据长度不匹配的情况
            min_length = min(len(result_df), len(time_series_data))
            logger.info(f"将使用最小长度进行数据对齐: {min_length}")
            
            for idx in range(min_length):
                # 获取结果数据
                if idx < len(result_df):
                    # 通过iloc获取第idx行，避免索引问题
                    row = result_df.iloc[idx]
                    value = float(row['value'])
                    anomaly_probability = float(row['anomaly_probability'])
                    is_anomaly = int(row['is_anomaly'])
                else:
                    # 如果result_df不够长，使用默认值
                    logger.warning(f"result_df索引{idx}不存在，使用默认值")
                    value = 0.0
                    anomaly_probability = 0.0
                    is_anomaly = 0
                
                # 获取原始数据的timestamp
                if idx < len(time_series_data):
                    original_data = time_series_data[idx]
                    timestamp = original_data.get('timestamp', f'index_{idx}')
                else:
                    # 如果原始数据不够长，生成默认timestamp
                    timestamp = f"index_{idx}"
                    logger.warning(f"原始数据索引{idx}不存在，使用默认timestamp")
                
                predictions.append({
                    'timestamp': timestamp,
                    'value': value,
                    'anomaly_probability': anomaly_probability,
                    'is_anomaly': is_anomaly
                })
            
            # 如果原始数据比结果数据长，为剩余的数据点添加默认预测
            if len(time_series_data) > len(result_df):
                logger.warning(f"原始数据比结果数据长，为剩余的{len(time_series_data) - len(result_df)}个数据点添加默认预测")
                for idx in range(len(result_df), len(time_series_data)):
                    original_data = time_series_data[idx]
                    predictions.append({
                        'timestamp': original_data.get('timestamp', f'index_{idx}'),
                        'value': float(original_data.get('value', 0.0)),
                        'anomaly_probability': 0.0,  # 默认概率
                        'is_anomaly': 0  # 默认非异常
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

        except IndexError as e:
            return Response(
                {'error': f'数据索引错误: {str(e)}，请检查输入数据格式和模型兼容性'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'推理失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
