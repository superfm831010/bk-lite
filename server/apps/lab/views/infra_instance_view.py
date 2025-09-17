# -*- coding: utf-8 -*-
"""
基础设施实例视图
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.lab.models import InfraInstance
from apps.lab.serializers import (
    InfraInstanceSerializer,
    InfraInstanceListSerializer,
    InfraInstanceCreateSerializer,
)


class InfraInstanceViewSet(viewsets.ModelViewSet):
    """
    基础设施实例视图集
    
    提供基础设施实例的增删改查功能
    """
    queryset = InfraInstance.objects.select_related('image').order_by('-created_at')
    serializer_class = InfraInstanceSerializer
    
    # 过滤和搜索
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'image', 'created_by']
    search_fields = ['name', 'image__name']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """根据动作选择不同的序列化器"""
        if self.action == 'list':
            return InfraInstanceListSerializer
        elif self.action == 'create':
            return InfraInstanceCreateSerializer
        return InfraInstanceSerializer
        
    def perform_create(self, serializer):
        """创建时设置创建者和初始状态"""
        serializer.save(
            created_by=getattr(self.request.user, 'username', 'system'),
            updated_by=getattr(self.request.user, 'username', 'system'),
            status='stopped'  # 新创建的实例默认为停止状态
        )
        
    def perform_update(self, serializer):
        """更新时设置更新者"""
        serializer.save(
            updated_by=getattr(self.request.user, 'username', 'system'),
        )
        
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """启动基础设施实例（占位实现）"""
        instance = self.get_object()
        
        if instance.status == 'running':
            return Response(
                {'detail': '实例已经在运行中'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: 实现实际的容器启动逻辑
        # 这里只是占位实现，实际应调用容器编排服务
        instance.status = 'starting'
        instance.save(update_fields=['status', 'updated_at'])
        
        return Response({
            'detail': '实例启动命令已发送',
            'status': instance.status,
            'message': '请稍后查看实例状态'
        })
        
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """停止基础设施实例（占位实现）"""
        instance = self.get_object()
        
        if instance.status == 'stopped':
            return Response(
                {'detail': '实例已经停止'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: 实现实际的容器停止逻辑
        # 这里只是占位实现，实际应调用容器编排服务
        instance.status = 'stopping'
        instance.save(update_fields=['status', 'updated_at'])
        
        return Response({
            'detail': '实例停止命令已发送',
            'status': instance.status,
            'message': '请稍后查看实例状态'
        })
        
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """获取实例日志（占位实现）"""
        instance = self.get_object()
        
        # TODO: 实现实际的日志获取逻辑
        return Response({
            'instance_name': instance.name,
            'logs': '暂无日志数据（功能开发中）',
            'message': '日志功能将在后续版本中实现'
        })
        
    @action(detail=False, methods=['get'])
    def running(self, request):
        """获取正在运行的实例列表"""
        running_instances = self.queryset.filter(status='running')
        serializer = InfraInstanceListSerializer(running_instances, many=True)
        return Response(serializer.data)