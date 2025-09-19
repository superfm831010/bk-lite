# -*- coding: utf-8 -*-
"""
容器编排示例配置

使用示例：
1. 在 .env 文件中设置环境变量
2. 或在 Django settings 中直接配置
"""

# ==================== Docker 配置示例 ====================
"""
# .env 文件示例
CONTAINER_ORCHESTRATOR=docker
DOCKER_HOST=unix:///var/run/docker.sock
DEFAULT_CPU_LIMIT=1
DEFAULT_MEMORY_LIMIT=1Gi
DEFAULT_NETWORK_PREFIX=bk-lite

# 使用 Docker 的配置，相同技术栈的容器会在同一个网络中运行
# 网络命名规则：bk-lite-{stack_name}-network
# 容器命名规则：{stack_name}-{service_name}-{instance_id}
"""

# ==================== Kubernetes 配置示例 ====================
"""
# .env 文件示例
CONTAINER_ORCHESTRATOR=kubernetes
K8S_NAMESPACE=bk-lite-lab
DEFAULT_CPU_LIMIT=1
DEFAULT_MEMORY_LIMIT=1Gi
DEFAULT_NETWORK_PREFIX=bk-lite

# 使用 Kubernetes 的配置，相同技术栈的服务会在同一个 namespace 中
# Deployment 命名规则：bk-lite-{stack_name}-{service_name}
# Service 命名规则：bk-lite-{stack_name}-{service_name}
# 网络访问：http://{service_name}.{namespace}.svc.cluster.local:{port}
"""

# ==================== Django Settings 配置示例 ====================
"""
# 在 settings.py 或配置文件中直接设置

# Docker 配置
CONTAINER_ORCHESTRATOR = 'docker'
CONTAINER_ORCHESTRATOR_CONFIG = {
    'docker_host': 'unix:///var/run/docker.sock',
    'default_cpu_limit': '1',
    'default_memory_limit': '1Gi',
    'default_network_prefix': 'bk-lite',
}

# 或者 Kubernetes 配置
CONTAINER_ORCHESTRATOR = 'kubernetes'
CONTAINER_ORCHESTRATOR_CONFIG = {
    'namespace': 'bk-lite-lab',
    'default_cpu_limit': '1',
    'default_memory_limit': '1Gi', 
    'default_network_prefix': 'bk-lite',
}
"""

# ==================== 技术栈网络设计 ====================
"""
Docker 模式：
- 技术栈：lamp（Linux + Apache + MySQL + PHP）
- 网络名称：bk-lite-lamp-network
- 容器：
  - lamp-apache-web01 (运行在 bk-lite-lamp-network)
  - lamp-mysql-db01 (运行在 bk-lite-lamp-network)
  - lamp-php-app01 (运行在 bk-lite-lamp-network)
- 容器间可通过容器名直接通信

Kubernetes 模式：
- 技术栈：lamp
- 命名空间：bk-lite-lab (或配置的命名空间)
- Deployment & Service：
  - bk-lite-lamp-apache (Service: bk-lite-lamp-apache)
  - bk-lite-lamp-mysql (Service: bk-lite-lamp-mysql) 
  - bk-lite-lamp-php (Service: bk-lite-lamp-php)
- 服务间通过 Service 名访问：http://bk-lite-lamp-mysql.bk-lite-lab.svc.cluster.local:3306
"""

# ==================== API 使用示例 ====================
"""
# 创建实例
POST /api/lab/infra-instances/
{
    "name": "lamp-mysql-db01",
    "image": 1,  # LabImage ID
    "env_vars": {
        "MYSQL_ROOT_PASSWORD": "password123",
        "MYSQL_DATABASE": "app_db"
    },
    "port_mappings": {
        "3306": "33060"
    },
    "cpu_limit": "1",
    "memory_limit": "2Gi"
}

# 启动实例
POST /api/lab/infra-instances/{id}/start/

# 停止实例  
POST /api/lab/infra-instances/{id}/stop/

# 获取日志
GET /api/lab/infra-instances/{id}/logs/?lines=100

# 同步状态
POST /api/lab/infra-instances/{id}/sync_status/
"""

# ==================== 注意事项 ====================
"""
1. 确保 Docker 或 Kubernetes 环境已正确安装和配置
2. 对于 Kubernetes，需要配置正确的 RBAC 权限
3. 容器镜像需要提前拉取或确保网络可访问镜像仓库
4. 持久化存储需要提前准备好挂载路径
5. 防火墙和网络策略需要允许容器间通信
6. 建议在生产环境中使用专门的命名空间或网络隔离
"""