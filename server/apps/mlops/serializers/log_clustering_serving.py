from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.log_clustering_serving import LogClusteringServing


class LogClusteringServingSerializer(AuthSerializer):
    """日志聚类服务序列化器"""
    permission_key = "dataset.log_clustering_serving"
    
    class Meta:
        model = LogClusteringServing
        fields = "__all__"