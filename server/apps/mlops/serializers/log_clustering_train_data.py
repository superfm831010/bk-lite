from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.log_clustering_train_data import LogClusteringTrainData


class LogClusteringTrainDataSerializer(AuthSerializer):
    """日志聚类训练数据序列化器"""
    permission_key = "dataset.log_clustering_train_data"
    
    class Meta:
        model = LogClusteringTrainData
        fields = "__all__"