from django_filters import FilterSet, CharFilter, DateTimeFilter, ChoiceFilter, NumberFilter

from apps.mlops.models.log_clustering_train_job import LogClusteringTrainJob


class LogClusteringTrainJobFilter(FilterSet):
    """日志聚类训练任务过滤器"""
    
    name = CharFilter(field_name="name", lookup_expr="icontains", label="任务名称")
    status = ChoiceFilter(
        field_name="status",
        choices=LogClusteringTrainJob._meta.get_field('status').choices,
        label="任务状态"
    )
    algorithm = ChoiceFilter(
        field_name="algorithm",
        choices=LogClusteringTrainJob._meta.get_field('algorithm').choices,
        label="算法模型"
    )
    train_data_id__name = CharFilter(field_name="train_data_id__name", lookup_expr="icontains", label="训练数据名称")
    cluster_count_min = NumberFilter(field_name="cluster_count", lookup_expr="gte", label="最小聚类数量")
    cluster_count_max = NumberFilter(field_name="cluster_count", lookup_expr="lte", label="最大聚类数量")
    created_by = CharFilter(field_name="created_by", lookup_expr="icontains", label="创建者")
    created_at_start = DateTimeFilter(field_name="created_at", lookup_expr="gte", label="创建时间开始")
    created_at_end = DateTimeFilter(field_name="created_at", lookup_expr="lte", label="创建时间结束")

    class Meta:
        model = LogClusteringTrainJob
        fields = ["name", "status", "algorithm", "train_data_id", "cluster_count", "created_by"]