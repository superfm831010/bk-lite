# -*- coding: utf-8 -*-
"""
Docker 配置 - MVP 简化版本
"""

import os

# Docker 网络前缀，用于创建技术栈网络
DOCKER_NETWORK_PREFIX = os.getenv('DOCKER_NETWORK_PREFIX', 'bk-lite')

# Docker 守护进程地址（可选）
DOCKER_HOST = os.getenv('DOCKER_HOST', None)