# -*- coding: utf-8 -*-
"""
Lab 环境序列化器
"""

from rest_framework import serializers
from apps.lab.models import LabEnv, LabImage, InfraInstance


class LabEnvSerializer(serializers.ModelSerializer):
    """Lab 环境序列化器"""
    
    state_display = serializers.CharField(source='get_state_display', read_only=True)
    ide_image_name = serializers.CharField(source='ide_image.name', read_only=True)
    ide_image_version = serializers.CharField(source='ide_image.version', read_only=True)
    
    # 关联的基础设施实例信息
    infra_instances_info = serializers.SerializerMethodField()
    
    class Meta:
        model = LabEnv
        fields = [
            'id', 'name', 'description', 'state', 'state_display', 'endpoint',
            'ide_image', 'ide_image_name', 'ide_image_version',
            'infra_instances', 'infra_instances_info',
            'cpu', 'memory', 'gpu', 'volume_size',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'state_display',
                           'ide_image_name', 'ide_image_version', 'endpoint',
                           'infra_instances_info']
        
    def get_infra_instances_info(self, obj):
        """获取关联的基础设施实例信息"""
        instances = obj.infra_instances.all()
        return [
            {
                'id': instance.id,
                'name': instance.name,
                'status': instance.status,
                'status_display': instance.get_status_display(),
                'image_name': instance.image.name,
                'image_version': instance.image.version,
                'endpoint': instance.endpoint
            }
            for instance in instances
        ]
        
    def validate_ide_image(self, value):
        """验证 IDE 镜像必须是 IDE 类型"""
        if value and value.image_type != 'ide':
            raise serializers.ValidationError('只能选择 IDE 类型的镜像')
        return value
        
    def validate_infra_instances(self, value):
        """验证基础设施实例"""
        for instance in value:
            if instance.image.image_type != 'infra':
                raise serializers.ValidationError(f'实例 {instance.name} 的镜像不是基础设施类型')
        return value
        
    def validate_cpu(self, value):
        """验证 CPU 配置"""
        if value < 1:
            raise serializers.ValidationError('CPU 核数不能小于 1')
        if value > 32:  # 合理的上限
            raise serializers.ValidationError('CPU 核数不能超过 32')
        return value
        
    def validate_gpu(self, value):
        """验证 GPU 配置"""
        if value < 0:
            raise serializers.ValidationError('GPU 数量不能小于 0')
        if value > 8:  # 合理的上限
            raise serializers.ValidationError('GPU 数量不能超过 8')
        return value


class LabEnvListSerializer(serializers.ModelSerializer):
    """Lab 环境列表序列化器（精简版）"""
    
    state_display = serializers.CharField(source='get_state_display', read_only=True)
    ide_image_name = serializers.CharField(source='ide_image.name', read_only=True)
    ide_image_version = serializers.CharField(source='ide_image.version', read_only=True)
    infra_instances_count = serializers.SerializerMethodField()
    
    class Meta:
        model = LabEnv
        fields = [
            'id', 'name', 'description', 'state', 'state_display',
            'ide_image_name', 'ide_image_version',
            'infra_instances_count', 'cpu', 'memory', 'gpu',
            'created_at'
        ]
        
    def get_infra_instances_count(self, obj):
        """获取关联的基础设施实例数量"""
        return obj.infra_instances.count()


class LabEnvCreateSerializer(serializers.ModelSerializer):
    """Lab 环境创建序列化器"""
    
    class Meta:
        model = LabEnv
        fields = [
            'name', 'description', 'ide_image', 'infra_instances',
            'cpu', 'memory', 'gpu', 'volume_size'
        ]
        
    def validate_ide_image(self, value):
        """验证 IDE 镜像必须是 IDE 类型"""
        if value and value.image_type != 'ide':
            raise serializers.ValidationError('只能选择 IDE 类型的镜像')
        return value