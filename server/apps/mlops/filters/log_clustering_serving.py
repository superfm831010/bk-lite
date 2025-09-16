from django_filters import FilterSet, CharFilter, DateTimeFilter, ChoiceFilter, NumberFilter

from apps.mlops.models.log_clustering_serving import LogClusteringServing


class LogClusteringServingFilter(FilterSet):
    """日志聚类服务过滤器"""
    
    name = CharFilter(field_name="name", lookup_expr="icontains", label="服务名称")
    status = ChoiceFilter(
        field_name="status",
        choices=LogClusteringServing._meta.get_field('status').choices,
        label="服务状态"
    )
    model_version = CharFilter(field_name="model_version", lookup_expr="icontains", label="模型版本")
    log_clustering_train_job__name = CharFilter(
        field_name="log_clustering_train_job__name", 
        lookup_expr="icontains", 
        label="训练任务名称"
    )
    api_endpoint = CharFilter(field_name="api_endpoint", lookup_expr="icontains", label="API端点")
    max_requests_per_minute_min = NumberFilter(field_name="max_requests_per_minute", lookup_expr="gte", label="最小请求频率")
    max_requests_per_minute_max = NumberFilter(field_name="max_requests_per_minute", lookup_expr="lte", label="最大请求频率")
    created_by = CharFilter(field_name="created_by", lookup_expr="icontains", label="创建者")
    created_at_start = DateTimeFilter(field_name="created_at", lookup_expr="gte", label="创建时间开始")
    created_at_end = DateTimeFilter(field_name="created_at", lookup_expr="lte", label="创建时间结束")

    class Meta:
        model = LogClusteringServing
        fields = ["name", "status", "model_version", "log_clustering_train_job", "api_endpoint", "max_requests_per_minute", "created_by"]