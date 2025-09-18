# -*- coding: utf-8 -*-
"""
容器编排服务抽象基类
定义统一的容器编排接口，支持 Docker 和 Kubernetes
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ContainerConfig:
    """容器配置"""
    name: str
    image: str
    ports: Dict[str, str]  # container_port: host_port
    environment: Dict[str, str]
    volumes: List[Dict[str, Any]]  # 卷挂载配置
    command: Optional[List[str]] = None
    args: Optional[List[str]] = None
    cpu_limit: Optional[str] = None
    memory_limit: Optional[str] = None
    extra_params: Optional[Dict[str, Any]] = None


@dataclass
class ContainerStatus:
    """容器状态"""
    name: str
    status: str  # running, stopped, starting, stopping, error
    endpoint: Optional[str] = None
    message: Optional[str] = None
    container_id: Optional[str] = None


class ContainerOrchestrator(ABC):
    """容器编排抽象基类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化容器编排器
        
        Args:
            config: 编排器配置参数
        """
        self.config = config or {}
        
    @abstractmethod
    async def start_container(self, config: ContainerConfig) -> ContainerStatus:
        """
        启动容器
        
        Args:
            config: 容器配置
            
        Returns:
            ContainerStatus: 容器状态
        """
        pass
        
    @abstractmethod
    async def stop_container(self, name: str) -> ContainerStatus:
        """
        停止容器
        
        Args:
            name: 容器名称
            
        Returns:
            ContainerStatus: 容器状态
        """
        pass
        
    @abstractmethod
    async def get_container_status(self, name: str) -> ContainerStatus:
        """
        获取容器状态
        
        Args:
            name: 容器名称
            
        Returns:
            ContainerStatus: 容器状态
        """
        pass
        
    @abstractmethod
    async def get_container_logs(self, name: str, lines: int = 100) -> str:
        """
        获取容器日志
        
        Args:
            name: 容器名称
            lines: 日志行数
            
        Returns:
            str: 容器日志
        """
        pass
        
    @abstractmethod
    async def remove_container(self, name: str) -> bool:
        """
        删除容器
        
        Args:
            name: 容器名称
            
        Returns:
            bool: 是否删除成功
        """
        pass
        
    def get_network_name(self, stack_name: str) -> str:
        """
        获取技术栈网络名称
        
        Args:
            stack_name: 技术栈名称
            
        Returns:
            str: 网络名称
        """
        return f"bk-lite-{stack_name}-network"
        
    def get_deployment_name(self, stack_name: str, service_name: str) -> str:
        """
        获取部署名称
        
        Args:
            stack_name: 技术栈名称
            service_name: 服务名称
            
        Returns:
            str: 部署名称
        """
        return f"bk-lite-{stack_name}-{service_name}"
        
    def validate_config(self, config: ContainerConfig) -> None:
        """
        验证容器配置
        
        Args:
            config: 容器配置
            
        Raises:
            ValueError: 配置验证失败
        """
        if not config.name:
            raise ValueError("容器名称不能为空")
        if not config.image:
            raise ValueError("镜像地址不能为空")


class ContainerOrchestratorFactory:
    """容器编排器工厂类"""
    
    _orchestrators = {}
    
    @classmethod
    def register(cls, name: str, orchestrator_class: type):
        """注册编排器"""
        cls._orchestrators[name] = orchestrator_class
        
    @classmethod
    def create(cls, orchestrator_type: str, config: Optional[Dict[str, Any]] = None) -> ContainerOrchestrator:
        """
        创建容器编排器
        
        Args:
            orchestrator_type: 编排器类型 (docker/kubernetes)
            config: 编排器配置
            
        Returns:
            ContainerOrchestrator: 容器编排器实例
        """
        if orchestrator_type not in cls._orchestrators:
            raise ValueError(f"不支持的编排器类型: {orchestrator_type}")
            
        orchestrator_class = cls._orchestrators[orchestrator_type]
        return orchestrator_class(config)
        
    @classmethod
    def get_available_orchestrators(cls) -> List[str]:
        """获取可用的编排器类型"""
        return list(cls._orchestrators.keys())