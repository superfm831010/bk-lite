import logging

import nats_client

from apps.node_mgmt.config_template.common import ConfigService
from apps.node_mgmt.services.node import NodeService

logger = logging.getLogger("app")


@nats_client.register
def node_list(query_data: dict):
    """获取节点列表"""
    organization_ids = query_data.get('organization_ids')
    cloud_region_id = query_data.get('cloud_region_id')
    name = query_data.get('name')
    ip = query_data.get('ip')
    os = query_data.get('os')
    page = query_data.get('page', 1)
    page_size = query_data.get('page_size', 10)
    return NodeService.get_node_list(organization_ids, cloud_region_id, name, ip, os, page, page_size)


@nats_client.register
def collector_list(query_data: dict):
    return []


@nats_client.register
def batch_add_node_child_config(data: dict):
    """批量添加子配置"""
    logger.info(f"batch_add_node_child_config: {data}")
    collector = data.get('collector')
    nodes = data.get('nodes')
    ConfigService().batch_add_child_config(collector, nodes)


@nats_client.register
def batch_add_node_config(data: dict):
    """批量添加配置"""
    logger.info(f"batch_add_exporter_config: {data}")
    collector = data.get('collector')
    nodes = data.get('nodes')
    ConfigService().batch_add_config(collector, nodes)


@nats_client.register
def get_child_configs_by_ids(ids: list):
    """根据ID获取子配置"""
    return ConfigService().get_child_configs_by_ids(ids)


@nats_client.register
def get_configs_by_ids(ids: list):
    """根据ID获取配置"""
    return ConfigService().get_configs_by_ids(ids)


@nats_client.register
def update_child_config_content(data: dict):
    """更新实例子配置"""
    id = data.get('id')
    content = data.get('content')
    ConfigService().update_child_config_content(id, content)


@nats_client.register
def update_config_content(data: dict):
    """更新配置内容"""
    id = data.get('id')
    content = data.get('content')
    ConfigService().update_config_content(id, content)


@nats_client.register
def delete_child_configs(ids: list):
    """删除实例子配置"""
    ConfigService().delete_child_configs(ids)


@nats_client.register
def delete_configs(ids: list):
    """删除实例子配置"""
    ConfigService().delete_configs(ids)