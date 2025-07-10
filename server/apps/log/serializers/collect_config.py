from rest_framework import serializers
from apps.log.models.collect_config import CollectType, CollectInstance, CollectConfig


class CollectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectType
        fields = '__all__'


class CollectInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectInstance
        fields = '__all__'


class CollectConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectConfig
        fields = '__all__'