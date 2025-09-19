# -*- coding: utf-8 -*-
"""
简单的 Docker 容器管理服务 - MVP 版本
专注核心功能：启动容器并确保同技术栈网络互通
"""

import subprocess
import json
import logging
from typing import Dict, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class SimpleDockerService:
    """简单的 Docker 服务 - MVP 实现"""
    
    def __init__(self):
        self.network_prefix = getattr(settings, 'DOCKER_NETWORK_PREFIX', 'bk-lite')
    
    def get_stack_network(self, instance_name: str) -> str:
        """从实例名获取技术栈网络名"""
        # 假设实例名格式：stack-service-id，如 lamp-mysql-01
        stack_name = instance_name.split('-')[0]
        return f"{self.network_prefix}-{stack_name}"
    
    def ensure_network(self, network_name: str) -> bool:
        """确保网络存在，不存在则创建"""
        try:
            # 检查网络是否存在
            result = subprocess.run([
                'docker', 'network', 'ls', '--filter', f'name={network_name}', '--format', '{{.Name}}'
            ], capture_output=True, text=True, check=True)
            
            if network_name in result.stdout:
                logger.info(f"网络 {network_name} 已存在")
                return True
            
            # 创建网络
            subprocess.run([
                'docker', 'network', 'create', network_name
            ], check=True)
            
            logger.info(f"已创建网络 {network_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"网络操作失败: {e}")
            return False
    
    def start_container(self, instance) -> Dict[str, str]:
        """启动容器 - 核心功能"""
        try:
            network_name = self.get_stack_network(instance.name)
            
            # 确保网络存在
            if not self.ensure_network(network_name):
                return {'status': 'error', 'message': '网络创建失败'}
            
            # 构建 docker run 命令
            cmd = [
                'docker', 'run', '-d',
                '--name', instance.name,
                '--network', network_name,
            ]
            
            # 端口映射
            if instance.port_mappings:
                for container_port, host_port in instance.port_mappings.items():
                    cmd.extend(['-p', f'{host_port}:{container_port}'])
            
            # 环境变量
            env_vars = {}
            if instance.image.default_env:
                env_vars.update(instance.image.default_env)
            if instance.env_vars:
                env_vars.update(instance.env_vars)
            
            for key, value in env_vars.items():
                cmd.extend(['-e', f'{key}={value}'])
            
            # 卷挂载
            if instance.volume_mounts:
                for volume in instance.volume_mounts:
                    host_path = volume.get('host_path')
                    container_path = volume.get('container_path')
                    if host_path and container_path:
                        cmd.extend(['-v', f'{host_path}:{container_path}'])
            
            # 镜像
            cmd.append(instance.image.image)
            
            # 启动命令
            if instance.command:
                cmd.extend(instance.command)
            elif instance.image.default_command:
                cmd.extend(instance.image.default_command)
            
            # 执行启动
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            container_id = result.stdout.strip()
            
            logger.info(f"容器 {instance.name} 启动成功: {container_id}")
            
            # 获取端点信息
            endpoint = self._get_container_endpoint(instance.name)
            
            return {
                'status': 'running',
                'message': '容器启动成功',
                'container_id': container_id,
                'endpoint': endpoint
            }
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            logger.error(f"启动容器失败 {instance.name}: {error_msg}")
            return {'status': 'error', 'message': error_msg}
        except Exception as e:
            logger.error(f"启动容器异常 {instance.name}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def stop_container(self, instance_name: str) -> Dict[str, str]:
        """停止容器"""
        try:
            subprocess.run(['docker', 'stop', instance_name], check=True)
            logger.info(f"容器 {instance_name} 停止成功")
            return {'status': 'stopped', 'message': '容器停止成功'}
        except subprocess.CalledProcessError as e:
            if 'No such container' in str(e):
                return {'status': 'stopped', 'message': '容器不存在'}
            logger.error(f"停止容器失败 {instance_name}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_container_status(self, instance_name: str) -> Dict[str, str]:
        """获取容器状态"""
        try:
            result = subprocess.run([
                'docker', 'inspect', instance_name, '--format', '{{.State.Status}}'
            ], capture_output=True, text=True, check=True)
            
            docker_status = result.stdout.strip()
            
            # 映射状态
            status_map = {
                'running': 'running',
                'exited': 'stopped',
                'created': 'starting',
                'dead': 'error'
            }
            
            status = status_map.get(docker_status, 'error')
            endpoint = self._get_container_endpoint(instance_name) if status == 'running' else None
            
            return {
                'status': status,
                'message': f'Docker状态: {docker_status}',
                'endpoint': endpoint
            }
            
        except subprocess.CalledProcessError:
            return {'status': 'stopped', 'message': '容器不存在'}
    
    def get_container_logs(self, instance_name: str, lines: int = 100) -> str:
        """获取容器日志"""
        try:
            result = subprocess.run([
                'docker', 'logs', '--tail', str(lines), instance_name
            ], capture_output=True, text=True, check=True)
            
            return result.stdout + result.stderr
            
        except subprocess.CalledProcessError as e:
            return f"获取日志失败: {e}"
    
    def _get_container_endpoint(self, instance_name: str) -> Optional[str]:
        """获取容器访问端点"""
        try:
            result = subprocess.run([
                'docker', 'port', instance_name
            ], capture_output=True, text=True, check=True)
            
            # 解析端口映射输出，格式如：3306/tcp -> 0.0.0.0:33060
            for line in result.stdout.strip().split('\n'):
                if '->' in line and '0.0.0.0' in line:
                    host_port = line.split('0.0.0.0:')[1]
                    return f"http://localhost:{host_port}"
                    
        except subprocess.CalledProcessError:
            pass
        
        return None