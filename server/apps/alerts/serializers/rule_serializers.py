from rest_framework import serializers
from apps.alerts.models import AggregationRules, CorrelationRules


class AggregationRulesSerializer(serializers.ModelSerializer):
    """聚合规则序列化器"""
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    correlation_name = serializers.SerializerMethodField()

    class Meta:
        model = AggregationRules
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'is_active': {'write_only': True},
            'severity': {'write_only': True},
            'template_title': {'write_only': True},
            'template_content': {'write_only': True},
            'condition': {'write_only': True},
        }

    @staticmethod
    def get_correlation_name(obj):
        """获取关联规则名称"""
        if getattr(obj, 'related_rules_names', None):
            return ",".join(i.name for i in obj.related_rules_names)
        return ""


class CorrelationRulesSerializer(serializers.ModelSerializer):
    """关联规则序列化器"""
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    exec_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    rule_names = serializers.SerializerMethodField()

    class Meta:
        model = CorrelationRules
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    @staticmethod
    def get_rule_names(obj):
        """获取关联规则名称列表"""
        if getattr(obj, 'related_rules_names', None):
            return ",".join(i.name for i in obj.related_rules_names)
        return ""
