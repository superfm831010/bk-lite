from django_filters import FilterSet, CharFilter, DateTimeFilter, ChoiceFilter

from apps.mlops.models.timeseries_predict_serving import TimeSeriesPredictServing


class TimeSeriesPredictServingFilter(FilterSet):
    """时间序列预测服务过滤器"""
    
    name = CharFilter(field_name="name", lookup_expr="icontains", label="服务名称")
    status = ChoiceFilter(
        field_name="status",
        choices=TimeSeriesPredictServing._meta.get_field('status').choices,
        label="服务状态"
    )
    model_version = CharFilter(field_name="model_version", lookup_expr="icontains", label="模型版本")
    time_series_predict_train_job__name = CharFilter(
        field_name="time_series_predict_train_job__name", 
        lookup_expr="icontains", 
        label="训练任务名称"
    )
    created_by = CharFilter(field_name="created_by", lookup_expr="icontains", label="创建者")
    created_at_start = DateTimeFilter(field_name="created_at", lookup_expr="gte", label="创建时间开始")
    created_at_end = DateTimeFilter(field_name="created_at", lookup_expr="lte", label="创建时间结束")

    class Meta:
        model = TimeSeriesPredictServing
        fields = ["name", "status", "model_version", "time_series_predict_train_job", "created_by"]