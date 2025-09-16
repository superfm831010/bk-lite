from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.timeseries_predict_dataset import TimeSeriesPredictDataset


class TimeSeriesPredictDatasetSerializer(AuthSerializer):
    """时间序列预测数据集序列化器"""
    permission_key = "dataset.timeseries_predict_dataset"
    
    class Meta:
        model = TimeSeriesPredictDataset
        fields = "__all__"