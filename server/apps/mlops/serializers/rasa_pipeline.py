from rest_framework import serializers

from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_pipeline import RasaPipeline
from apps.mlops.models.rasa_dataset import RasaDatasets


class RasaPipelineSerializer(AuthSerializer):
    """Rasa训练管道序列化器"""
    permission_key = "dataset.rasa_pipeline"

    # 数据集数量统计
    dataset_count = serializers.SerializerMethodField(read_only=True, help_text="关联数据集数量")
    
    # 数据集名称列表
    dataset_names = serializers.SerializerMethodField(read_only=True, help_text="关联数据集名称列表")
    
    # 多对多字段处理，用于写入
    datasets = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=RasaDatasets.objects.all(),
        required=False,
        help_text="关联的数据集ID列表"
    )

    class Meta:
        model = RasaPipeline
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True, 'help_text': '管道名称，必须唯一'},
            'description': {'required': False, 'help_text': '管道描述'},
            'config': {'required': False, 'help_text': 'Rasa pipeline配置JSON'},
            'datasets': {'write_only': True, 'help_text': '关联数据集ID列表'},
        }

    def get_dataset_count(self, obj):
        """
        获取关联的数据集数量
        """
        return obj.get_dataset_count()

    def get_dataset_names(self, obj):
        """
        获取关联的数据集名称列表
        """
        return obj.get_dataset_names()

    def validate_name(self, value):
        """
        验证管道名称的唯一性
        """
        if self.instance:
            # 更新时，排除当前实例
            if RasaPipeline.objects.exclude(id=self.instance.id).filter(name=value).exists():
                raise serializers.ValidationError("管道名称已存在")
        else:
            # 创建时
            if RasaPipeline.objects.filter(name=value).exists():
                raise serializers.ValidationError("管道名称已存在")
        return value

    def validate_config(self, value):
        """
        验证配置JSON格式
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError("配置必须是有效的JSON对象")
        
        # 可以在这里添加更多的配置验证逻辑
        # 例如检查必要的配置项是否存在
        if value and 'pipeline' not in value:
            raise serializers.ValidationError("配置中必须包含'pipeline'字段")
        
        return value

    def validate_datasets(self, value):
        """
        验证关联的数据集
        """
        if not value:
            return value
        
        # 检查数据集是否存在
        dataset_ids = [dataset.id for dataset in value]
        existing_datasets = RasaDatasets.objects.filter(id__in=dataset_ids)
        if len(existing_datasets) != len(dataset_ids):
            raise serializers.ValidationError("部分数据集不存在")
        
        return value

    def create(self, validated_data):
        """
        创建新的管道实例
        """
        datasets = validated_data.pop('datasets', [])
        pipeline = RasaPipeline.objects.create(**validated_data)
        
        # 设置多对多关系
        if datasets:
            pipeline.datasets.set(datasets)
        
        return pipeline

    def update(self, instance, validated_data):
        """
        更新管道实例
        """
        datasets = validated_data.pop('datasets', None)
        
        # 更新基本字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 更新多对多关系
        if datasets is not None:
            instance.datasets.set(datasets)
        
        return instance

    def to_representation(self, instance):
        """
        自定义序列化输出，包含数据集详细信息
        """
        response = super().to_representation(instance)
        
        # 添加关联数据集的详细信息
        if hasattr(instance, 'datasets'):
            datasets_data = []
            for dataset in instance.datasets.all():
                datasets_data.append({
                    'id': dataset.id,
                    'name': dataset.name,
                    'description': dataset.description,
                    'created_at': dataset.created_at.strftime('%Y-%m-%d %H:%M:%S') if dataset.created_at else None,
                })
            response['datasets_detail'] = datasets_data
        
        return response


class RasaPipelineSimpleSerializer(serializers.ModelSerializer):
    """
    简单的管道序列化器，用于选择列表等场景
    """
    dataset_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RasaPipeline
        fields = ['id', 'name', 'description', 'dataset_count', 'created_at', 'updated_at']

    def get_dataset_count(self, obj):
        return obj.get_dataset_count()
