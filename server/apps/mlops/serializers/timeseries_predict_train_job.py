from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.timeseries_predict_train_job import TimeSeriesPredictTrainJob


class TimeSeriesPredictTrainJobSerializer(AuthSerializer):
    """时间序列预测训练任务序列化器"""
    permission_key = "dataset.timeseries_predict_train_job"
    
    class Meta:
        model = TimeSeriesPredictTrainJob
        fields = "__all__"