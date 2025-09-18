# -*- coding: utf-8 -*-
"""
基础设施实例视图 - MVP 简化版本
"""

import logging
from django.conf import settings
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
from apps.lab.services.simple_docker import SimpleDockerService

logger = logging.getLogger(__name__)


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
        
    def get_docker_service(self):
        """获取 Docker 服务实例"""
        return SimpleDockerService()
        
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
            
            # 更新实例状态
            instance.status = result['status']
            if result.get('endpoint'):
                instance.endpoint = result['endpoint']
            instance.save(update_fields=['status', 'endpoint', 'updated_at'])
            
            return Response({
                'detail': '实例启动命令已发送',
                'status': instance.status,
                'endpoint': instance.endpoint,
                'message': result.get('message', '启动中')
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
        
    async def stop_container_async(self, instance: InfraInstance):
        """异步停止容器"""
        try:
            # 获取容器编排器
            orchestrator_type = self.get_orchestrator_type()
            orchestrator_config = self.get_orchestrator_config()
            orchestrator = ContainerOrchestratorFactory.create(
                orchestrator_type, 
                orchestrator_config
            )
            
            # 停止容器
            container_status = await orchestrator.stop_container(instance.name)
            
            # 更新实例状态
            status_mapping = {
                'running': 'running',
                'starting': 'starting', 
                'stopped': 'stopped',
                'stopping': 'stopping',
                'error': 'error'
            }
            
            instance.status = status_mapping.get(container_status.status, 'error')
            instance.save(update_fields=['status', 'updated_at'])
            
            return container_status
            
        except Exception as e:
            logger.error(f"停止容器失败 {instance.name}: {e}")
            instance.status = 'error'
            instance.save(update_fields=['status', 'updated_at'])
            raise
        
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
            # 先设置状态为停止中
            instance.status = 'stopping'
            instance.save(update_fields=['status', 'updated_at'])
            
            # 停止容器
            container_status = run_async_in_thread(self.stop_container_async(instance))
            
            return Response({
                'detail': '实例停止命令已发送',
                'status': instance.status,
                'message': container_status.message if container_status else '停止中，请稍后查看实例状态'
            })
            
        except Exception as e:
            logger.error(f"停止实例失败 {instance.name}: {e}")
            return Response(
                {
                    'detail': '停止实例失败',
                    'error': str(e),
                    'status': instance.status
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    async def get_container_logs_async(self, instance: InfraInstance, lines: int = 100):
        """异步获取容器日志"""
        try:
            # 获取容器编排器
            orchestrator_type = self.get_orchestrator_type()
            orchestrator_config = self.get_orchestrator_config()
            orchestrator = ContainerOrchestratorFactory.create(
                orchestrator_type, 
                orchestrator_config
            )
            
            # 获取日志
            logs = await orchestrator.get_container_logs(instance.name, lines)
            return logs
            
        except Exception as e:
            logger.error(f"获取容器日志失败 {instance.name}: {e}")
            return f"获取日志失败: {str(e)}"
        
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """获取实例日志"""
        instance = self.get_object()
        lines = int(request.query_params.get('lines', 100))
        
        try:
            logs = run_async_in_thread(self.get_container_logs_async(instance, lines))
            
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
        
    async def sync_container_status_async(self, instance: InfraInstance):
        """异步同步容器状态"""
        try:
            # 获取容器编排器
            orchestrator_type = self.get_orchestrator_type()
            orchestrator_config = self.get_orchestrator_config()
            orchestrator = ContainerOrchestratorFactory.create(
                orchestrator_type, 
                orchestrator_config
            )
            
            # 获取容器状态
            container_status = await orchestrator.get_container_status(instance.name)
            
            # 更新实例状态
            status_mapping = {
                'running': 'running',
                'starting': 'starting', 
                'stopped': 'stopped',
                'stopping': 'stopping',
                'error': 'error'
            }
            
            old_status = instance.status
            instance.status = status_mapping.get(container_status.status, 'error')
            if container_status.endpoint:
                instance.endpoint = container_status.endpoint
                
            instance.save(update_fields=['status', 'endpoint', 'updated_at'])
            
            return {
                'old_status': old_status,
                'new_status': instance.status,
                'endpoint': instance.endpoint,
                'message': container_status.message
            }
            
        except Exception as e:
            logger.error(f"同步容器状态失败 {instance.name}: {e}")
            raise
        
    @action(detail=True, methods=['post'])
    def sync_status(self, request, pk=None):
        """同步容器状态"""
        instance = self.get_object()
        
        try:
            result = run_async_in_thread(self.sync_container_status_async(instance))
            
            return Response({
                'detail': '状态同步完成',
                'instance_name': instance.name,
                'old_status': result['old_status'],
                'new_status': result['new_status'],
                'endpoint': result['endpoint'],
                'message': result['message']
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