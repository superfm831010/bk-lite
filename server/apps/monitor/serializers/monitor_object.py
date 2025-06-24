from rest_framework import serializers

from apps.monitor.models.monitor_object import MonitorObject, MonitorObjectOrganizationRule


class MonitorObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorObject
        fields = '__all__'


class MonitorObjectOrganizationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorObjectOrganizationRule
        fields = '__all__'
