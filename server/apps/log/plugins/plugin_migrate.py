import os
import json

from apps.core.logger import monitor_logger as logger
from apps.rpc.node_mgmt import NodeMgmt

PLUGIN_DIRECTORY = 'apps/log/plugins'

def migrate_collector():
    """迁移采集器"""
    collectors_path = []
    for type_name in os.listdir(PLUGIN_DIRECTORY):
        type_path = os.path.join(PLUGIN_DIRECTORY, type_name)
        if not os.path.isdir(type_path):
            continue
        for config_name in os.listdir(type_path):
            if config_name == "collectors.json":
                config_path = os.path.join(type_path, config_name)
                collectors_path.append(config_path)
                continue

    for file_path in collectors_path:
        # 打开并读取 JSON 文件
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                collectors_data = json.load(file)
                NodeMgmt().collectors_import(collectors_data)
        except Exception as e:
            logger.error(f'导入采集器 {file_path} 失败！原因：{e}')
