from attr import fields
from apps.core.utils.serializers import AuthSerializer
from rest_framework import serializers
from apps.mlops.models.anomaly_detection_train_data import AnomalyDetectionTrainData


class AnomalyDetectionTrainDataSerializer(AuthSerializer):
    
    permission_key = "dataset.anomaly_detection_train_data"
    
    class Meta:
        model = AnomalyDetectionTrainData
        fields = "__all__"  # 允许新增时包含所有字段
        extra_kwargs = {
            'name': {'required': False},
            'train_data': {'required': False},
            'dataset': {'required': False},
        }

    def __init__(self, *args, **kwargs):
        """
        初始化序列化器，从请求上下文中获取 include_train_data 参数
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            self.include_train_data = request.query_params.get('include_train_data', 'false').lower() == 'true'
            self.include_metadata = request.query_params.get('include_metadata', 'false').lower() == 'true'
        else:
            self.include_train_data = False
            self.include_metadata = False

    def to_representation(self, instance):
        """
        自定义返回数据，根据 include_train_data 参数动态控制 train_data 字段
        """
        representation = super().to_representation(instance)
        if not self.include_train_data:
            representation.pop("train_data", None)  # 移除 train_data 字段
        if not self.include_metadata:
            representation.pop("metadata", None)  # 移除 metadata 字段
        return representation
