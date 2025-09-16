from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.log_clustering_train_job import LogClusteringTrainJob


class LogClusteringTrainJobSerializer(AuthSerializer):
    """日志聚类训练任务序列化器"""
    permission_key = "dataset.log_clustering_train_job"
    
    class Meta:
        model = LogClusteringTrainJob
        fields = "__all__"