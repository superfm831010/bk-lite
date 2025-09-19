from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.timeseries_predict_train_data import TimeSeriesPredictTrainData


class TimeSeriesPredictTrainDataSerializer(AuthSerializer):
    """时间序列预测训练数据序列化器"""
    permission_key = "dataset.timeseries_predict_train_data"
    
    class Meta:
        model = TimeSeriesPredictTrainData
        fields = "__all__"