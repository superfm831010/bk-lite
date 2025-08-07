from rest_framework import serializers
from apps.log.models.policy import Policy, Alert, Event, EventRawData


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'last_run_time')

    def validate_name(self, value):
        """验证策略名称唯一性"""
        if self.instance:
            # 更新时排除当前实例
            if Policy.objects.filter(
                name=value,
                collect_type=self.instance.collect_type
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("该采集方式下策略名称已存在")
        else:
            # 创建时检查
            collect_type = self.initial_data.get('collect_type')
            if collect_type and Policy.objects.filter(name=value, collect_type=collect_type).exists():
                raise serializers.ValidationError("该采集方式下策略名称已存在")
        return value


class AlertSerializer(serializers.ModelSerializer):
    policy_name = serializers.CharField(source='policy.name', read_only=True)
    collect_type_name = serializers.CharField(source='collect_type.name', read_only=True)

    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class EventSerializer(serializers.ModelSerializer):
    policy_name = serializers.CharField(source='policy.name', read_only=True)
    alert_id = serializers.CharField(source='alert.id', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class EventRawDataSerializer(serializers.ModelSerializer):
    event_id = serializers.CharField(source='event.id', read_only=True)

    class Meta:
        model = EventRawData
        fields = '__all__'
