from rest_framework import serializers
from apps.log.models import CollectType, CollectInstance, CollectConfig


class CollectTypeSerializer(serializers.ModelSerializer):
    policy_count = serializers.SerializerMethodField()
    instance_count = serializers.SerializerMethodField()

    class Meta:
        model = CollectType
        fields = '__all__'

    def get_policy_count(self, obj):
        """
        获取当前采集类型下的策略数量
        优先使用annotate计算的结果，避免额外的数据库查询
        """
        request = self.context.get('request')
        if request and request.query_params.get('add_policy_count', '').lower() in ['true', '1']:
            # 如果queryset已经通过annotate计算了policy_count，直接使用
            if hasattr(obj, 'policy_count'):
                return obj.policy_count
            # 兜底方案：如果没有annotate，则进行单独查询（不推荐但保证兼容性）
            return obj.policy_set.count()
        return None

    def get_instance_count(self, obj):
        """
        获取当前采集类型下的实例数量
        优先使用annotate计算的结果，避免额外的数据库查询
        """
        request = self.context.get('request')
        if request and request.query_params.get('add_instance_count', '').lower() in ['true', '1']:
            # 如果queryset已经通过annotate计算了instance_count，直接使用
            if hasattr(obj, 'instance_count'):
                return obj.instance_count
            # 兜底方案：如果没有annotate，则进行单独查询（不推荐但保证兼容性）
            return obj.collectinstance_set.count()
        return None


class CollectInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectInstance
        fields = '__all__'


class CollectConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectConfig
        fields = '__all__'