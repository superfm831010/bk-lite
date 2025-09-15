from django_filters import FilterSet, CharFilter, DateTimeFilter, BooleanFilter, NumberFilter

from apps.mlops.models.log_clustering_train_data import LogClusteringTrainData


class LogClusteringTrainDataFilter(FilterSet):
    """日志聚类训练数据过滤器"""
    
    name = CharFilter(field_name="name", lookup_expr="icontains", label="训练数据名称")
    dataset__name = CharFilter(field_name="dataset__name", lookup_expr="icontains", label="数据集名称")
    is_train_data = BooleanFilter(field_name="is_train_data", label="是否为训练数据")
    is_val_data = BooleanFilter(field_name="is_val_data", label="是否为验证数据")
    is_test_data = BooleanFilter(field_name="is_test_data", label="是否为测试数据")
    log_count_min = NumberFilter(field_name="log_count", lookup_expr="gte", label="最小日志条数")
    log_count_max = NumberFilter(field_name="log_count", lookup_expr="lte", label="最大日志条数")
    log_source = CharFilter(field_name="log_source", lookup_expr="icontains", label="日志来源")
    created_by = CharFilter(field_name="created_by", lookup_expr="icontains", label="创建者")
    created_at_start = DateTimeFilter(field_name="created_at", lookup_expr="gte", label="创建时间开始")
    created_at_end = DateTimeFilter(field_name="created_at", lookup_expr="lte", label="创建时间结束")

    class Meta:
        model = LogClusteringTrainData
        fields = ["name", "dataset", "is_train_data", "is_val_data", "is_test_data", "log_count", "log_source", "created_by"]