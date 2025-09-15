from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.timeseries_predict_serving import TimeSeriesPredictServing


class TimeSeriesPredictServingSerializer(AuthSerializer):
    """时间序列预测服务序列化器"""
    permission_key = "dataset.timeseries_predict_serving"
    
    class Meta:
        model = TimeSeriesPredictServing
        fields = "__all__"