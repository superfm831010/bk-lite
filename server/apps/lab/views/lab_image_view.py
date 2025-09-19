# -*- coding: utf-8 -*-
"""
Lab 镜像视图
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.lab.models import LabImage
from apps.lab.serializers import (
    LabImageSerializer,
    LabImageListSerializer,
)


class LabImageViewSet(viewsets.ModelViewSet):
    """
    Lab 镜像视图集
    
    提供镜像的增删改查功能
    """
    queryset = LabImage.objects.all().order_by('-created_at')
    serializer_class = LabImageSerializer
    
    # 过滤和搜索
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['image_type', 'created_by']
    search_fields = ['name', 'version', 'description', 'image']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """根据动作选择不同的序列化器"""
        if self.action == 'list':
            return LabImageListSerializer
        return LabImageSerializer
        
    def perform_create(self, serializer):
        """创建时设置创建者"""
        serializer.save(
            created_by=getattr(self.request.user, 'username', 'system'),
            updated_by=getattr(self.request.user, 'username', 'system'),
        )
        
    def perform_update(self, serializer):
        """更新时设置更新者"""
        serializer.save(
            updated_by=getattr(self.request.user, 'username', 'system'),
        )
        
    @action(detail=False, methods=['get'])
    def ide_images(self, request):
        """获取 IDE 镜像列表"""
        ide_images = self.queryset.filter(image_type='ide')
        serializer = LabImageListSerializer(ide_images, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def infra_images(self, request):
        """获取基础设施镜像列表"""
        infra_images = self.queryset.filter(image_type='infra')
        serializer = LabImageListSerializer(infra_images, many=True)
        return Response(serializer.data)
        
    @action(detail=True, methods=['get'])
    def instances(self, request, pk=None):
        """获取使用该镜像的所有实例"""
        image = self.get_object()
        if image.image_type == 'ide':
            # IDE 镜像关联的 Lab 环境
            lab_envs = image.lab_envs.all()
            data = [
                {
                    'id': env.id,
                    'name': env.name,
                    'type': 'lab_env',
                    'state': env.state,
                    'state_display': env.get_state_display(),
                    'created_at': env.created_at,
                }
                for env in lab_envs
            ]
        else:
            # 基础设施镜像关联的实例
            instances = image.instances.all()
            data = [
                {
                    'id': instance.id,
                    'name': instance.name,
                    'type': 'infra_instance',
                    'status': instance.status,
                    'status_display': instance.get_status_display(),
                    'created_at': instance.created_at,
                }
                for instance in instances
            ]
        
        return Response(data)