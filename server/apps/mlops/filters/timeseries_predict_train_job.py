from django_filters import FilterSet, CharFilter, DateTimeFilter, ChoiceFilter

from apps.mlops.models.timeseries_predict_train_job import TimeSeriesPredictTrainJob


class TimeSeriesPredictTrainJobFilter(FilterSet):
    """时间序列预测训练任务过滤器"""
    
    name = CharFilter(field_name="name", lookup_expr="icontains", label="任务名称")
    status = ChoiceFilter(
        field_name="status",
        choices=TimeSeriesPredictTrainJob._meta.get_field('status').choices,
        label="任务状态"
    )
    algorithm = ChoiceFilter(
        field_name="algorithm",
        choices=TimeSeriesPredictTrainJob._meta.get_field('algorithm').choices,
        label="算法模型"
    )
    train_data_id__name = CharFilter(field_name="train_data_id__name", lookup_expr="icontains", label="训练数据名称")
    created_by = CharFilter(field_name="created_by", lookup_expr="icontains", label="创建者")
    created_at_start = DateTimeFilter(field_name="created_at", lookup_expr="gte", label="创建时间开始")
    created_at_end = DateTimeFilter(field_name="created_at", lookup_expr="lte", label="创建时间结束")

    class Meta:
        model = TimeSeriesPredictTrainJob
        fields = ["name", "status", "algorithm", "train_data_id", "created_by"]