# -*- coding: utf-8 -*-
"""
Lab 镜像序列化器
"""

from rest_framework import serializers
from apps.lab.models import LabImage


class LabImageSerializer(serializers.ModelSerializer):
    """Lab 镜像序列化器"""
    
    image_type_display = serializers.CharField(source='get_image_type_display', read_only=True)
    
    class Meta:
        model = LabImage
        fields = [
            'id', 'name', 'version', 'image_type', 'image_type_display',
            'description', 'image', 'default_port', 'default_env',
            'default_command', 'default_args', 'expose_ports', 'volume_mounts',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'image_type_display']
        
    def validate(self, attrs):
        """自定义验证"""
        # 验证镜像地址格式
        image = attrs.get('image', '')
        if image and not any(char in image for char in [':', '/']):
            raise serializers.ValidationError({
                'image': '镜像地址格式不正确，应包含仓库地址或标签'
            })
            
        # 验证端口范围
        default_port = attrs.get('default_port')
        if default_port and not (1 <= default_port <= 65535):
            raise serializers.ValidationError({
                'default_port': '端口号必须在 1-65535 范围内'
            })
            
        return attrs


class LabImageListSerializer(serializers.ModelSerializer):
    """Lab 镜像列表序列化器（精简版）"""
    
    image_type_display = serializers.CharField(source='get_image_type_display', read_only=True)
    
    class Meta:
        model = LabImage
        fields = [
            'id', 'name', 'version', 'image_type', 'image_type_display',
            'description', 'image', 'default_port', 'created_at'
        ]