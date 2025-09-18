# -*- coding: utf-8 -*-
"""
Docker 容器编排服务
使用 Docker Python SDK 管理容器
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any

import docker
from docker.errors import DockerException, ImageNotFound, ContainerError

from .container_orchestrator import (
    ContainerOrchestrator,
    ContainerConfig,
    ContainerStatus,
    ContainerOrchestratorFactory,
)

logger = logging.getLogger(__name__)


class DockerOrchestrator(ContainerOrchestrator):
    """Docker 容器编排器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化 Docker 编排器
        
        Args:
            config: Docker 配置参数
        """
        super().__init__(config)
        try:
            self.client = docker.from_env()
            # 测试连接
            self.client.ping()
            logger.info("Docker 客户端连接成功")
        except DockerException as e:
            logger.error(f"Docker 客户端连接失败: {e}")
            raise
            
    async def start_container(self, config: ContainerConfig) -> ContainerStatus:
        """
        启动 Docker 容器
        
        Args:
            config: 容器配置
            
        Returns:
            ContainerStatus: 容器状态
        """
        try:
            self.validate_config(config)
            
            # 检查容器是否已存在
            existing_container = await self._get_existing_container(config.name)
            if existing_container:
                if existing_container.status == 'running':
                    return ContainerStatus(
                        name=config.name,
                        status='running',
                        message='容器已在运行中',
                        container_id=existing_container.id
                    )
                else:
                    # 启动已存在的容器
                    existing_container.start()
                    return await self._get_container_status_from_container(existing_container)
            
            # 创建或获取网络
            network = await self._ensure_network(config)
            
            # 准备容器配置
            container_config = await self._prepare_container_config(config, network)
            
            # 拉取镜像（如果本地不存在）
            await self._pull_image_if_needed(config.image)
            
            # 创建并启动容器
            container = self.client.containers.run(
                **container_config,
                detach=True,
                name=config.name
            )
            
            logger.info(f"成功启动容器: {config.name}")
            return await self._get_container_status_from_container(container)
            
        except Exception as e:
            logger.error(f"启动容器失败 {config.name}: {e}")
            return ContainerStatus(
                name=config.name,
                status='error',
                message=str(e)
            )
            
    async def stop_container(self, name: str) -> ContainerStatus:
        """
        停止 Docker 容器
        
        Args:
            name: 容器名称
            
        Returns:
            ContainerStatus: 容器状态
        """
        try:
            container = await self._get_existing_container(name)
            if not container:
                return ContainerStatus(
                    name=name,
                    status='stopped',
                    message='容器不存在'
                )
                
            if container.status == 'running':
                container.stop(timeout=30)
                logger.info(f"成功停止容器: {name}")
                
            return await self._get_container_status_from_container(container)
            
        except Exception as e:
            logger.error(f"停止容器失败 {name}: {e}")
            return ContainerStatus(
                name=name,
                status='error',
                message=str(e)
            )
            
    async def get_container_status(self, name: str) -> ContainerStatus:
        """
        获取容器状态
        
        Args:
            name: 容器名称
            
        Returns:
            ContainerStatus: 容器状态
        """
        try:
            container = await self._get_existing_container(name)
            if not container:
                return ContainerStatus(
                    name=name,
                    status='stopped',
                    message='容器不存在'
                )
                
            return await self._get_container_status_from_container(container)
            
        except Exception as e:
            logger.error(f"获取容器状态失败 {name}: {e}")
            return ContainerStatus(
                name=name,
                status='error',
                message=str(e)
            )
            
    async def get_container_logs(self, name: str, lines: int = 100) -> str:
        """
        获取容器日志
        
        Args:
            name: 容器名称
            lines: 日志行数
            
        Returns:
            str: 容器日志
        """
        try:
            container = await self._get_existing_container(name)
            if not container:
                return f"容器 {name} 不存在"
                
            logs = container.logs(tail=lines, timestamps=True)
            return logs.decode('utf-8', errors='ignore')
            
        except Exception as e:
            logger.error(f"获取容器日志失败 {name}: {e}")
            return f"获取日志失败: {str(e)}"
            
    async def remove_container(self, name: str) -> bool:
        """
        删除容器
        
        Args:
            name: 容器名称
            
        Returns:
            bool: 是否删除成功
        """
        try:
            container = await self._get_existing_container(name)
            if not container:
                return True
                
            # 先停止容器
            if container.status == 'running':
                container.stop(timeout=30)
                
            # 删除容器
            container.remove()
            logger.info(f"成功删除容器: {name}")
            return True
            
        except Exception as e:
            logger.error(f"删除容器失败 {name}: {e}")
            return False
            
    async def _get_existing_container(self, name: str):
        """获取已存在的容器"""
        try:
            return self.client.containers.get(name)
        except docker.errors.NotFound:
            return None
            
    async def _ensure_network(self, config: ContainerConfig):
        """确保网络存在"""
        # 根据容器名称推断技术栈名称（假设格式为 stack-service-xxx）
        stack_name = config.name.split('-')[0] if '-' in config.name else 'default'
        network_name = self.get_network_name(stack_name)
        
        try:
            return self.client.networks.get(network_name)
        except docker.errors.NotFound:
            # 创建新的网络
            network = self.client.networks.create(
                name=network_name,
                driver="bridge",
                labels={"bk-lite.stack": stack_name}
            )
            logger.info(f"创建网络: {network_name}")
            return network
            
    async def _prepare_container_config(self, config: ContainerConfig, network) -> Dict[str, Any]:
        """准备容器配置"""
        container_config = {
            'image': config.image,
            'environment': config.environment,
            'network': network.name,
            'labels': {
                'bk-lite.managed': 'true',
                'bk-lite.instance': config.name,
            }
        }
        
        # 端口映射
        if config.ports:
            ports = {}
            port_bindings = {}
            for container_port, host_port in config.ports.items():
                # 格式化端口
                container_port_str = f"{container_port}/tcp"
                ports[container_port_str] = {}
                port_bindings[container_port_str] = [{'HostPort': host_port}]
                
            container_config['ports'] = ports
            container_config['port_bindings'] = port_bindings
            
        # 卷挂载
        if config.volumes:
            volumes = {}
            binds = []
            for volume in config.volumes:
                host_path = volume.get('host_path')
                container_path = volume.get('container_path')
                read_only = volume.get('read_only', False)
                
                if host_path and container_path:
                    volumes[container_path] = {}
                    bind_config = f"{host_path}:{container_path}"
                    if read_only:
                        bind_config += ":ro"
                    binds.append(bind_config)
                    
            if volumes:
                container_config['volumes'] = volumes
            if binds:
                container_config['binds'] = binds
                
        # 启动命令
        if config.command:
            container_config['command'] = config.command
            
        # 资源限制
        if config.cpu_limit or config.memory_limit:
            host_config = {}
            if config.cpu_limit:
                # CPU 限制 (例如: "1.5" -> 1.5 * 1e9 nanocpus)
                cpu_quota = int(float(config.cpu_limit) * 100000)
                host_config['cpu_quota'] = cpu_quota
                host_config['cpu_period'] = 100000
                
            if config.memory_limit:
                # 内存限制 (例如: "1Gi" -> bytes)
                memory_bytes = self._parse_memory_limit(config.memory_limit)
                host_config['mem_limit'] = memory_bytes
                
            container_config['host_config'] = host_config
            
        return container_config
        
    async def _pull_image_if_needed(self, image: str):
        """如果本地不存在则拉取镜像"""
        try:
            self.client.images.get(image)
        except ImageNotFound:
            logger.info(f"拉取镜像: {image}")
            self.client.images.pull(image)
            
    async def _get_container_status_from_container(self, container) -> ContainerStatus:
        """从容器对象获取状态"""
        container.reload()  # 刷新容器状态
        
        # 映射 Docker 状态到我们的状态
        docker_status = container.status.lower()
        if docker_status == 'running':
            status = 'running'
        elif docker_status in ['exited', 'dead']:
            status = 'stopped'
        elif docker_status in ['created', 'restarting']:
            status = 'starting'
        else:
            status = 'error'
            
        # 获取访问端点
        endpoint = None
        if status == 'running' and container.ports:
            # 尝试获取第一个映射的端口
            for port_info in container.ports.values():
                if port_info:
                    host_port = port_info[0].get('HostPort')
                    if host_port:
                        endpoint = f"http://localhost:{host_port}"
                        break
                        
        return ContainerStatus(
            name=container.name,
            status=status,
            endpoint=endpoint,
            message=f"Docker 状态: {docker_status}",
            container_id=container.id
        )
        
    def _parse_memory_limit(self, memory_str: str) -> int:
        """解析内存限制字符串转为字节数"""
        memory_str = memory_str.strip().upper()
        
        if memory_str.endswith('B'):
            memory_str = memory_str[:-1]
            
        multipliers = {
            'K': 1024,
            'M': 1024 ** 2,
            'G': 1024 ** 3,
            'KI': 1024,
            'MI': 1024 ** 2,
            'GI': 1024 ** 3,
        }
        
        for suffix, multiplier in multipliers.items():
            if memory_str.endswith(suffix):
                return int(float(memory_str[:-len(suffix)]) * multiplier)
                
        # 如果没有单位，假设是字节
        return int(memory_str)


# 注册 Docker 编排器
ContainerOrchestratorFactory.register('docker', DockerOrchestrator)