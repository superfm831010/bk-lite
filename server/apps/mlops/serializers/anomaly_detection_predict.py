from rest_framework import serializers
from typing import List, Dict, Any


class TimeSeriesDataSerializer(serializers.Serializer):
    """时序数据点序列化器"""
    timestamp = serializers.CharField(help_text="时间戳，格式: YYYY-MM-DD HH:MM:SS")
    value = serializers.FloatField(help_text="数值")
    label = serializers.IntegerField(required=False, help_text="标签（可选）")


class AnomalyDetectionPredictRequestSerializer(serializers.Serializer):
    """异常检测预测请求序列化器"""
    model_name = serializers.CharField(
        max_length=100,
        help_text="模型名称"
    )
    model_version = serializers.CharField(
        max_length=50,
        default="latest",
        help_text="模型版本，默认为latest"
    )
    algorithm = serializers.ChoiceField(
        choices=[('RandomForest', 'RandomForest')],
        help_text="算法类型"
    )
    data = TimeSeriesDataSerializer(
        many=True,
        help_text="时序数据列表"
    )
    anomaly_threshold = serializers.FloatField(
        default=0.5,
        min_value=0.0,
        max_value=1.0,
        help_text="异常判定阈值，范围[0,1]"
    )

    def validate_data(self, value):
        """验证时序数据"""
        if not value:
            raise serializers.ValidationError("数据不能为空")
        if len(value) < 2:
            raise serializers.ValidationError("至少需要2个数据点")
        return value


class PredictionResultSerializer(serializers.Serializer):
    """单个预测结果序列化器"""
    timestamp = serializers.CharField(help_text="时间戳")
    value = serializers.FloatField(help_text="原始数值")
    anomaly_probability = serializers.FloatField(help_text="异常概率")
    is_anomaly = serializers.IntegerField(help_text="是否异常，1为异常，0为正常")


class AnomalyDetectionPredictResponseSerializer(serializers.Serializer):
    """异常检测预测响应序列化器"""
    success = serializers.BooleanField(help_text="预测是否成功")
    model_name = serializers.CharField(help_text="使用的模型名称")
    model_version = serializers.CharField(help_text="使用的模型版本")
    algorithm = serializers.CharField(help_text="使用的算法")
    anomaly_threshold = serializers.FloatField(help_text="异常判定阈值")
    total_points = serializers.IntegerField(help_text="总数据点数")
    anomaly_count = serializers.IntegerField(help_text="异常点数量")
    predictions = PredictionResultSerializer(
        many=True,
        help_text="预测结果列表"
    )
