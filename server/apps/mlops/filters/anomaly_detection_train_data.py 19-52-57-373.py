from django_filters import FilterSet, CharFilter, BooleanFilter, NumberFilter
from apps.mlops.models.anomaly_detection_train_data import AnomalyDetectionTrainData


class AnomalyDetectionTrainDataFilter(FilterSet):
    """异常检测训练数据过滤器"""
    
    name = CharFilter(field_name="name", lookup_expr="icontains", label="训练数据名称")
    dataset = NumberFilter(field_name="dataset__id", label="数据集ID")
    dataset_name = CharFilter(field_name="dataset__name", lookup_expr="icontains", label="数据集名称")
    is_train_data = BooleanFilter(field_name="is_train_data", label="是否为训练数据")
    is_val_data = BooleanFilter(field_name="is_val_data", label="是否为验证数据")
    is_test_data = BooleanFilter(field_name="is_test_data", label="是否为测试数据")

    class Meta:
        model = AnomalyDetectionTrainData
        fields = [
            "name", "dataset", "dataset_name", 
            "is_train_data", "is_val_data", "is_test_data"
        ]