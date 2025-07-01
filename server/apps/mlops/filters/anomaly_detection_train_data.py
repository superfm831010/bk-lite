from apps.mlops.models.anomaly_detection_train_data import AnomalyDetectionTrainData
from django_filters.rest_framework import FilterSet


class AnomalyDetectionTrainDataFilter(FilterSet):
    """异常检测训练数据过滤器"""

    class Meta:
        model = AnomalyDetectionTrainData
        fields = {
            "name": ["exact", "icontains"],
            "dataset": ["exact"],  # 支持按数据集ID进行精确匹配过滤
        }

   