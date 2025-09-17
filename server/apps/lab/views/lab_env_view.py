# -*- coding: utf-8 -*-
"""
Lab 环境视图
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.lab.models import LabEnv
from apps.lab.serializers import (
    LabEnvSerializer,
    LabEnvListSerializer,
    LabEnvCreateSerializer,
)


class LabEnvViewSet(viewsets.ModelViewSet):
    """
    Lab 环境视图集
    
    提供实验环境的增删改查、启动、停止功能
    """
    queryset = LabEnv.objects.select_related('ide_image').prefetch_related('infra_instances').order_by('-created_at')
    serializer_class = LabEnvSerializer
    
    # 过滤和搜索
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['state', 'ide_image', 'created_by']
    search_fields = ['name', 'description', 'ide_image__name']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """根据动作选择不同的序列化器"""
        if self.action == 'list':
            return LabEnvListSerializer
        elif self.action == 'create':
            return LabEnvCreateSerializer
        return LabEnvSerializer
        
    def perform_create(self, serializer):
        """创建时设置创建者和初始状态"""
        serializer.save(
            created_by=getattr(self.request.user, 'username', 'system'),
            updated_by=getattr(self.request.user, 'username', 'system'),
            state='stopped'  # 新创建的环境默认为停止状态
        )
        
    def perform_update(self, serializer):
        """更新时设置更新者"""
        serializer.save(
            updated_by=getattr(self.request.user, 'username', 'system'),
        )
        
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """启动 Lab 环境（占位实现）"""
        lab_env = self.get_object()
        
        if lab_env.state == 'running':
            return Response(
                {'detail': 'Lab 环境已经在运行中'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: 实现实际的环境启动逻辑
        # 1. 先启动关联的基础设施实例
        # 2. 等待基础设施实例就绪
        # 3. 启动 IDE 容器
        # 4. 配置网络和存储
        # 5. 生成访问端点
        
        lab_env.state = 'starting'
        lab_env.save(update_fields=['state', 'updated_at'])
        
        return Response({
            'detail': 'Lab 环境启动命令已发送',
            'state': lab_env.state,
            'message': '环境启动中，请稍后查看状态。完整的启动逻辑将在后续版本中实现。'
        })
        
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """停止 Lab 环境（占位实现）"""
        lab_env = self.get_object()
        
        if lab_env.state == 'stopped':
            return Response(
                {'detail': 'Lab 环境已经停止'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: 实现实际的环境停止逻辑
        # 1. 停止 IDE 容器
        # 2. 停止关联的基础设施实例（如果不被其他环境使用）
        # 3. 清理网络配置
        # 4. 保留持久化数据
        
        lab_env.state = 'stopping'
        lab_env.endpoint = None  # 清空访问端点
        lab_env.save(update_fields=['state', 'endpoint', 'updated_at'])
        
        return Response({
            'detail': 'Lab 环境停止命令已发送',
            'state': lab_env.state,
            'message': '环境停止中，请稍后查看状态。完整的停止逻辑将在后续版本中实现。'
        })
        
    @action(detail=True, methods=['post'])
    def restart(self, request, pk=None):
        """重启 Lab 环境（占位实现）"""
        lab_env = self.get_object()
        
        # TODO: 实现重启逻辑（先停止再启动）
        lab_env.state = 'starting'
        lab_env.save(update_fields=['state', 'updated_at'])
        
        return Response({
            'detail': 'Lab 环境重启命令已发送',
            'state': lab_env.state,
            'message': '环境重启中，请稍后查看状态'
        })
        
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """获取环境详细状态"""
        lab_env = self.get_object()
        
        # 获取关联基础设施实例的状态
        infra_status = []
        for instance in lab_env.infra_instances.all():
            infra_status.append({
                'id': instance.id,
                'name': instance.name,
                'status': instance.status,
                'status_display': instance.get_status_display(),
                'endpoint': instance.endpoint,
            })
        
        return Response({
            'id': lab_env.id,
            'name': lab_env.name,
            'state': lab_env.state,
            'state_display': lab_env.get_state_display(),
            'endpoint': lab_env.endpoint,
            'ide_image': {
                'name': lab_env.ide_image.name,
                'version': lab_env.ide_image.version,
            },
            'infra_instances': infra_status,
            'resources': {
                'cpu': lab_env.cpu,
                'memory': lab_env.memory,
                'gpu': lab_env.gpu,
                'volume_size': lab_env.volume_size,
            },
            'created_at': lab_env.created_at,
            'updated_at': lab_env.updated_at,
        })
        
    @action(detail=False, methods=['get'])
    def running(self, request):
        """获取正在运行的环境列表"""
        running_envs = self.queryset.filter(state='running')
        serializer = LabEnvListSerializer(running_envs, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """获取环境统计摘要"""
        total = self.queryset.count()
        running = self.queryset.filter(state='running').count()
        stopped = self.queryset.filter(state='stopped').count()
        starting = self.queryset.filter(state='starting').count()
        stopping = self.queryset.filter(state='stopping').count()
        error = self.queryset.filter(state='error').count()
        
        return Response({
            'total': total,
            'running': running,
            'stopped': stopped,
            'starting': starting,
            'stopping': stopping,
            'error': error,
        })