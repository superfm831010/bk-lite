# -*- coding: utf-8 -*-
"""
基础设施实例序列化器
"""

from rest_framework import serializers
from apps.lab.models import InfraInstance, LabImage


class InfraInstanceSerializer(serializers.ModelSerializer):
    """基础设施实例序列化器"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    image_name = serializers.CharField(source='image.name', read_only=True)
    image_version = serializers.CharField(source='image.version', read_only=True)
    
    class Meta:
        model = InfraInstance
        fields = [
            'id', 'name', 'status', 'status_display', 'endpoint',
            'image', 'image_name', 'image_version',
            'env_vars', 'command', 'args', 'port_mappings',
            'volume_mounts', 'persistent_dirs',
            'cpu_limit', 'memory_limit', 'extra_params',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status_display', 
                           'image_name', 'image_version', 'endpoint']
        
    def validate_image(self, value):
        """验证镜像必须是基础设施类型"""
        if value and value.image_type != 'infra':
            raise serializers.ValidationError('只能选择基础设施类型的镜像')
        return value
        
    def validate_port_mappings(self, value):
        """验证端口映射格式"""
        if not isinstance(value, dict):
            raise serializers.ValidationError('端口映射必须是字典格式')
            
        for container_port, host_port in value.items():
            try:
                container_port_int = int(container_port)
                host_port_int = int(host_port)
                if not (1 <= container_port_int <= 65535) or not (1 <= host_port_int <= 65535):
                    raise serializers.ValidationError('端口号必须在 1-65535 范围内')
            except ValueError:
                raise serializers.ValidationError('端口必须是数字')
                
        return value
        
    def validate_volume_mounts(self, value):
        """验证卷挂载配置"""
        if not isinstance(value, list):
            raise serializers.ValidationError('卷挂载配置必须是列表格式')
            
        for mount in value:
            if not isinstance(mount, dict):
                raise serializers.ValidationError('每个挂载配置必须是字典格式')
            required_fields = ['host_path', 'container_path']
            for field in required_fields:
                if field not in mount:
                    raise serializers.ValidationError(f'挂载配置缺少必需字段: {field}')
                    
        return value


class InfraInstanceListSerializer(serializers.ModelSerializer):
    """基础设施实例列表序列化器（精简版）"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    image_name = serializers.CharField(source='image.name', read_only=True)
    image_version = serializers.CharField(source='image.version', read_only=True)
    
    class Meta:
        model = InfraInstance
        fields = [
            'id', 'name', 'status', 'status_display', 'endpoint',
            'image', 'image_name', 'image_version', 'created_at'
        ]


class InfraInstanceCreateSerializer(serializers.ModelSerializer):
    """基础设施实例创建序列化器"""
    
    class Meta:
        model = InfraInstance
        fields = [
            'name', 'image', 'env_vars', 'command', 'args',
            'port_mappings', 'volume_mounts', 'persistent_dirs',
            'cpu_limit', 'memory_limit', 'extra_params'
        ]
        
    def validate_image(self, value):
        """验证镜像必须是基础设施类型"""
        if value and value.image_type != 'infra':
            raise serializers.ValidationError('只能选择基础设施类型的镜像')
        return value