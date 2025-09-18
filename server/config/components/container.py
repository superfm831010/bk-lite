# -*- coding: utf-8 -*-
"""
容器编排相关配置
"""

import os

# 容器编排器类型：docker 或 kubernetes
CONTAINER_ORCHESTRATOR = os.getenv('CONTAINER_ORCHESTRATOR', 'docker')

# 容器编排器配置
CONTAINER_ORCHESTRATOR_CONFIG = {
    # Kubernetes 配置
    'namespace': os.getenv('K8S_NAMESPACE', 'default'),
    
    # Docker 配置
    'docker_host': os.getenv('DOCKER_HOST'),
    
    # 通用配置
    'default_cpu_limit': os.getenv('DEFAULT_CPU_LIMIT', '1'),
    'default_memory_limit': os.getenv('DEFAULT_MEMORY_LIMIT', '1Gi'),
    'default_network_prefix': os.getenv('DEFAULT_NETWORK_PREFIX', 'bk-lite'),
}