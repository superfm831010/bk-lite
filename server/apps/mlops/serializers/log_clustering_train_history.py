from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.log_clustering_train_history import LogClusteringTrainHistory


class LogClusteringTrainHistorySerializer(AuthSerializer):
    """日志聚类训练历史序列化器"""
    permission_key = "dataset.log_clustering_train_history"
    
    class Meta:
        model = LogClusteringTrainHistory
        fields = "__all__"