from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.timeseries_predict_train_history import TimeSeriesPredictTrainHistory


class TimeSeriesPredictTrainHistorySerializer(AuthSerializer):
    """时间序列预测训练历史序列化器"""
    permission_key = "dataset.timeseries_predict_train_history"
    
    class Meta:
        model = TimeSeriesPredictTrainHistory
        fields = "__all__"