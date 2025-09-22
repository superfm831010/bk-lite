# -*- coding: utf-8 -*-
"""
基础设施实例视图 - MVP 简化版本
专注核心功能：启动/停止容器，确保同技术栈网络互通
"""

import logging
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

logger = logging.getLogger(__name__)


class InfraInstanceViewSet(viewsets.ModelViewSet):
    """
    基础设施实例视图集 - MVP 版本
    
    提供基础设施实例的增删改查功能，专注 Docker 容器管理
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
        
    def get_docker_service(self):
        """获取 Docker 服务实例"""
        return None
        
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """启动基础设施实例"""
        instance = self.get_object()
        
        if instance.status == 'running':
            return Response(
                {'detail': '实例已经在运行中'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 设置状态为启动中
            instance.status = 'starting'
            instance.save(update_fields=['status', 'updated_at'])
            
            # 启动容器
            docker_service = self.get_docker_service()
            result = docker_service.start_container(instance)
            
            # 更新实例状态和端点
            instance.status = result['status']
            if result.get('endpoint'):
                instance.endpoint = result['endpoint']
            instance.save(update_fields=['status', 'endpoint', 'updated_at'])
            
            return Response({
                'detail': '实例启动完成',
                'status': instance.status,
                'endpoint': instance.endpoint,
                'message': result.get('message', ''),
                'container_id': result.get('container_id')
            })
            
        except Exception as e:
            logger.error(f"启动实例失败 {instance.name}: {e}")
            instance.status = 'error'
            instance.save(update_fields=['status', 'updated_at'])
            return Response(
                {
                    'detail': '启动实例失败',
                    'error': str(e),
                    'status': instance.status
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """停止基础设施实例"""
        instance = self.get_object()
        
        if instance.status == 'stopped':
            return Response(
                {'detail': '实例已经停止'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 停止容器
            docker_service = self.get_docker_service()
            result = docker_service.stop_container(instance.name)
            
            # 更新实例状态
            instance.status = result['status']
            instance.endpoint = None  # 清除端点信息
            instance.save(update_fields=['status', 'endpoint', 'updated_at'])
            
            return Response({
                'detail': '实例停止完成',
                'status': instance.status,
                'message': result.get('message', '')
            })
            
        except Exception as e:
            logger.error(f"停止实例失败 {instance.name}: {e}")
            return Response(
                {
                    'detail': '停止实例失败',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """获取实例日志"""
        instance = self.get_object()
        lines = int(request.query_params.get('lines', 100))
        
        try:
            docker_service = self.get_docker_service()
            logs = docker_service.get_container_logs(instance.name, lines)
            
            return Response({
                'instance_name': instance.name,
                'logs': logs,
                'lines': lines
            })
            
        except Exception as e:
            logger.error(f"获取实例日志失败 {instance.name}: {e}")
            return Response(
                {
                    'detail': '获取日志失败',
                    'error': str(e),
                    'instance_name': instance.name
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=True, methods=['post'])
    def sync_status(self, request, pk=None):
        """同步容器状态"""
        instance = self.get_object()
        
        try:
            docker_service = self.get_docker_service()
            result = docker_service.get_container_status(instance.name)
            
            old_status = instance.status
            instance.status = result['status']
            if result.get('endpoint'):
                instance.endpoint = result['endpoint']
            elif result['status'] == 'stopped':
                instance.endpoint = None
                
            instance.save(update_fields=['status', 'endpoint', 'updated_at'])
            
            return Response({
                'detail': '状态同步完成',
                'instance_name': instance.name,
                'old_status': old_status,
                'new_status': instance.status,
                'endpoint': instance.endpoint,
                'message': result.get('message', '')
            })
            
        except Exception as e:
            logger.error(f"同步实例状态失败 {instance.name}: {e}")
            return Response(
                {
                    'detail': '同步状态失败',
                    'error': str(e),
                    'instance_name': instance.name
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['get'])
    def running(self, request):
        """获取正在运行的实例列表"""
        running_instances = self.queryset.filter(status='running')
        serializer = InfraInstanceListSerializer(running_instances, many=True)
        return Response(serializer.data)