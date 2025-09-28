from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.log_clustering_dataset import LogClusteringDataset


class LogClusteringDatasetSerializer(AuthSerializer):
    """日志聚类数据集序列化器"""
    permission_key = "dataset.log_clustering_dataset"
    
    class Meta:
        model = LogClusteringDataset
        fields = "__all__"