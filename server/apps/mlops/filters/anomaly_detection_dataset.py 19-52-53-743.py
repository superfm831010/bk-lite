from django_filters import FilterSet, CharFilter, DateTimeFilter

from apps.mlops.models.anomaly_detection_dataset import AnomalyDetectionDataset


class AnomalyDetectionDatasetFilter(FilterSet):
    """异常检测数据集过滤器"""
    
    name = CharFilter(field_name="name", lookup_expr="icontains", label="数据集名称")
    created_by = CharFilter(field_name="created_by", lookup_expr="icontains", label="创建者")
    created_at_start = DateTimeFilter(field_name="created_at", lookup_expr="gte", label="创建时间开始")
    created_at_end = DateTimeFilter(field_name="created_at", lookup_expr="lte", label="创建时间结束")

    class Meta:
        model = AnomalyDetectionDataset
        fields = ["name", "created_by"]
