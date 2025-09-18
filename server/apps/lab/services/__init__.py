# -*- coding: utf-8 -*-
"""
容器编排服务模块
提供统一的容器编排接口，支持 Docker 和 Kubernetes
"""

from .container_orchestrator import (
    ContainerOrchestrator,
    ContainerConfig,
    ContainerStatus,
    ContainerOrchestratorFactory,
)

# 导入具体实现以注册到工厂
from .docker_orchestrator import DockerOrchestrator
from .kubernetes_orchestrator import KubernetesOrchestrator

__all__ = [
    'ContainerOrchestrator',
    'ContainerConfig', 
    'ContainerStatus',
    'ContainerOrchestratorFactory',
    'DockerOrchestrator',
    'KubernetesOrchestrator',
]
