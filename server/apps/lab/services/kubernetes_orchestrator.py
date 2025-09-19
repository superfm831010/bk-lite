# -*- coding: utf-8 -*-
"""
Kubernetes 容器编排服务
使用 Kubernetes Python Client 管理容器
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any

from kubernetes import client, config
from kubernetes.client.rest import ApiException

from .container_orchestrator import (
    ContainerOrchestrator,
    ContainerConfig,
    ContainerStatus,
    ContainerOrchestratorFactory,
)

logger = logging.getLogger(__name__)


class KubernetesOrchestrator(ContainerOrchestrator):
    """Kubernetes 容器编排器"""
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        初始化 Kubernetes 编排器
        
        Args:
            config_dict: Kubernetes 配置参数
        """
        super().__init__(config_dict)
        
        try:
            # 尝试加载集群内配置
            try:
                config.load_incluster_config()
                logger.info("使用集群内 Kubernetes 配置")
            except config.ConfigException:
                # 如果不在集群内，尝试加载本地配置
                config.load_kube_config()
                logger.info("使用本地 Kubernetes 配置")
                
            # 初始化客户端
            self.apps_v1 = client.AppsV1Api()
            self.core_v1 = client.CoreV1Api()
            self.namespace = config_dict.get('namespace', 'default') if config_dict else 'default'
            
            logger.info(f"Kubernetes 客户端初始化成功，命名空间: {self.namespace}")
            
        except Exception as e:
            logger.error(f"Kubernetes 客户端初始化失败: {e}")
            raise
            
    async def start_container(self, config: ContainerConfig) -> ContainerStatus:
        """
        启动 Kubernetes Deployment
        
        Args:
            config: 容器配置
            
        Returns:
            ContainerStatus: 容器状态
        """
        try:
            self.validate_config(config)
            
            # 根据容器名称推断技术栈名称
            stack_name = config.name.split('-')[0] if '-' in config.name else 'default'
            service_name = config.name.split('-', 1)[1] if '-' in config.name else config.name
            
            deployment_name = self.get_deployment_name(stack_name, service_name)
            
            # 检查 Deployment 是否已存在
            existing_deployment = await self._get_existing_deployment(deployment_name)
            if existing_deployment:
                # 如果已存在且副本数大于0，说明正在运行
                if existing_deployment.spec.replicas > 0:
                    return ContainerStatus(
                        name=config.name,
                        status='running',
                        message='Deployment 已在运行中'
                    )
                else:
                    # 扩容到1个副本
                    await self._scale_deployment(deployment_name, 1)
                    return ContainerStatus(
                        name=config.name,
                        status='starting',
                        message='Deployment 扩容中'
                    )
            
            # 创建新的 Deployment
            deployment = await self._create_deployment(config, stack_name, service_name)
            
            # 创建 Service
            service = await self._create_service(config, stack_name, service_name)
            
            logger.info(f"成功创建 Deployment: {deployment_name}")
            
            return ContainerStatus(
                name=config.name,
                status='starting',
                message='Deployment 创建中',
                endpoint=await self._get_service_endpoint(service.metadata.name)
            )
            
        except Exception as e:
            logger.error(f"启动容器失败 {config.name}: {e}")
            return ContainerStatus(
                name=config.name,
                status='error',
                message=str(e)
            )
            
    async def stop_container(self, name: str) -> ContainerStatus:
        """
        停止 Kubernetes Deployment (通过缩放到0)
        
        Args:
            name: 容器名称
            
        Returns:
            ContainerStatus: 容器状态
        """
        try:
            # 根据容器名称推断部署名称
            stack_name = name.split('-')[0] if '-' in name else 'default'
            service_name = name.split('-', 1)[1] if '-' in name else name
            deployment_name = self.get_deployment_name(stack_name, service_name)
            
            # 检查 Deployment 是否存在
            deployment = await self._get_existing_deployment(deployment_name)
            if not deployment:
                return ContainerStatus(
                    name=name,
                    status='stopped',
                    message='Deployment 不存在'
                )
            
            # 缩放到0个副本
            await self._scale_deployment(deployment_name, 0)
            
            logger.info(f"成功停止 Deployment: {deployment_name}")
            
            return ContainerStatus(
                name=name,
                status='stopping',
                message='Deployment 缩容中'
            )
            
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
            # 根据容器名称推断部署名称
            stack_name = name.split('-')[0] if '-' in name else 'default'
            service_name = name.split('-', 1)[1] if '-' in name else name
            deployment_name = self.get_deployment_name(stack_name, service_name)
            
            # 获取 Deployment
            deployment = await self._get_existing_deployment(deployment_name)
            if not deployment:
                return ContainerStatus(
                    name=name,
                    status='stopped',
                    message='Deployment 不存在'
                )
            
            # 分析状态
            replicas = deployment.spec.replicas or 0
            ready_replicas = deployment.status.ready_replicas or 0
            
            if replicas == 0:
                status = 'stopped'
                message = 'Deployment 已停止'
            elif ready_replicas == replicas:
                status = 'running'
                message = f'Deployment 运行中 ({ready_replicas}/{replicas})'
            else:
                status = 'starting'
                message = f'Deployment 启动中 ({ready_replicas}/{replicas})'
            
            # 获取服务端点
            service_name_k8s = f"bk-lite-{stack_name}-{service_name}"
            endpoint = await self._get_service_endpoint(service_name_k8s)
            
            return ContainerStatus(
                name=name,
                status=status,
                message=message,
                endpoint=endpoint
            )
            
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
            # 根据容器名称推断标签选择器
            stack_name = name.split('-')[0] if '-' in name else 'default'
            service_name = name.split('-', 1)[1] if '-' in name else name
            
            label_selector = f"bk-lite.stack={stack_name},bk-lite.service={service_name}"
            
            # 获取 Pod 列表
            pods = self.core_v1.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=label_selector
            )
            
            if not pods.items:
                return f"未找到容器 {name} 的 Pod"
            
            # 获取第一个 Pod 的日志
            pod = pods.items[0]
            logs = self.core_v1.read_namespaced_pod_log(
                name=pod.metadata.name,
                namespace=self.namespace,
                tail_lines=lines
            )
            
            return logs
            
        except Exception as e:
            logger.error(f"获取容器日志失败 {name}: {e}")
            return f"获取日志失败: {str(e)}"
            
    async def remove_container(self, name: str) -> bool:
        """
        删除容器 (删除 Deployment 和 Service)
        
        Args:
            name: 容器名称
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 根据容器名称推断资源名称
            stack_name = name.split('-')[0] if '-' in name else 'default'
            service_name = name.split('-', 1)[1] if '-' in name else name
            deployment_name = self.get_deployment_name(stack_name, service_name)
            service_name_k8s = f"bk-lite-{stack_name}-{service_name}"
            
            # 删除 Deployment
            try:
                await self.apps_v1.delete_namespaced_deployment(
                    name=deployment_name,
                    namespace=self.namespace
                )
                logger.info(f"已删除 Deployment: {deployment_name}")
            except ApiException as e:
                if e.status != 404:  # 忽略不存在的错误
                    raise
                    
            # 删除 Service
            try:
                await self.core_v1.delete_namespaced_service(
                    name=service_name_k8s,
                    namespace=self.namespace
                )
                logger.info(f"已删除 Service: {service_name_k8s}")
            except ApiException as e:
                if e.status != 404:  # 忽略不存在的错误
                    raise
                    
            return True
            
        except Exception as e:
            logger.error(f"删除容器失败 {name}: {e}")
            return False
            
    async def _get_existing_deployment(self, deployment_name: str):
        """获取已存在的 Deployment"""
        try:
            return self.apps_v1.read_namespaced_deployment(
                name=deployment_name,
                namespace=self.namespace
            )
        except ApiException as e:
            if e.status == 404:
                return None
            raise
            
    async def _scale_deployment(self, deployment_name: str, replicas: int):
        """缩放 Deployment"""
        body = {
            'spec': {
                'replicas': replicas
            }
        }
        
        return self.apps_v1.patch_namespaced_deployment_scale(
            name=deployment_name,
            namespace=self.namespace,
            body=body
        )
        
    async def _create_deployment(self, config: ContainerConfig, stack_name: str, service_name: str):
        """创建 Deployment"""
        deployment_name = self.get_deployment_name(stack_name, service_name)
        
        # 准备容器规格
        container_spec = client.V1Container(
            name=service_name,
            image=config.image,
            env=[
                client.V1EnvVar(name=k, value=v)
                for k, v in config.environment.items()
            ]
        )
        
        # 端口配置
        if config.ports:
            container_spec.ports = [
                client.V1ContainerPort(container_port=int(port))
                for port in config.ports.keys()
            ]
            
        # 启动命令
        if config.command:
            container_spec.command = config.command
        if config.args:
            container_spec.args = config.args
            
        # 资源限制
        if config.cpu_limit or config.memory_limit:
            resources = client.V1ResourceRequirements()
            limits = {}
            if config.cpu_limit:
                limits['cpu'] = config.cpu_limit
            if config.memory_limit:
                limits['memory'] = config.memory_limit
            resources.limits = limits
            container_spec.resources = resources
            
        # 卷挂载
        if config.volumes:
            volume_mounts = []
            volumes = []
            
            for i, volume in enumerate(config.volumes):
                volume_name = f"volume-{i}"
                mount = client.V1VolumeMount(
                    name=volume_name,
                    mount_path=volume['container_path'],
                    read_only=volume.get('read_only', False)
                )
                volume_mounts.append(mount)
                
                # 使用 hostPath 卷
                vol = client.V1Volume(
                    name=volume_name,
                    host_path=client.V1HostPathVolumeSource(
                        path=volume['host_path']
                    )
                )
                volumes.append(vol)
                
            container_spec.volume_mounts = volume_mounts
        else:
            volumes = []
            
        # Pod 模板
        pod_template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={
                    'bk-lite.managed': 'true',
                    'bk-lite.stack': stack_name,
                    'bk-lite.service': service_name,
                    'bk-lite.instance': config.name,
                }
            ),
            spec=client.V1PodSpec(
                containers=[container_spec],
                volumes=volumes
            )
        )
        
        # Deployment 规格
        deployment_spec = client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={
                    'bk-lite.stack': stack_name,
                    'bk-lite.service': service_name,
                }
            ),
            template=pod_template
        )
        
        # Deployment 对象
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(
                name=deployment_name,
                labels={
                    'bk-lite.managed': 'true',
                    'bk-lite.stack': stack_name,
                    'bk-lite.service': service_name,
                }
            ),
            spec=deployment_spec
        )
        
        return self.apps_v1.create_namespaced_deployment(
            namespace=self.namespace,
            body=deployment
        )
        
    async def _create_service(self, config: ContainerConfig, stack_name: str, service_name: str):
        """创建 Service"""
        service_name_k8s = f"bk-lite-{stack_name}-{service_name}"
        
        # 端口配置
        ports = []
        if config.ports:
            for container_port, host_port in config.ports.items():
                port = client.V1ServicePort(
                    name=f"port-{container_port}",
                    port=int(host_port),
                    target_port=int(container_port),
                    protocol="TCP"
                )
                ports.append(port)
        
        # Service 规格
        service_spec = client.V1ServiceSpec(
            selector={
                'bk-lite.stack': stack_name,
                'bk-lite.service': service_name,
            },
            ports=ports,
            type="ClusterIP"  # 使用 ClusterIP，同一个 namespace 内的服务可以互相访问
        )
        
        # Service 对象
        service = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(
                name=service_name_k8s,
                labels={
                    'bk-lite.managed': 'true',
                    'bk-lite.stack': stack_name,
                    'bk-lite.service': service_name,
                }
            ),
            spec=service_spec
        )
        
        return self.core_v1.create_namespaced_service(
            namespace=self.namespace,
            body=service
        )
        
    async def _get_service_endpoint(self, service_name: str) -> Optional[str]:
        """获取服务端点"""
        try:
            service = self.core_v1.read_namespaced_service(
                name=service_name,
                namespace=self.namespace
            )
            
            if service.spec.ports:
                port = service.spec.ports[0].port
                # 在 Kubernetes 中，同一命名空间的服务可以通过服务名访问
                return f"http://{service_name}.{self.namespace}.svc.cluster.local:{port}"
                
        except ApiException as e:
            if e.status != 404:
                logger.error(f"获取服务端点失败: {e}")
                
        return None


# 注册 Kubernetes 编排器
ContainerOrchestratorFactory.register('kubernetes', KubernetesOrchestrator)