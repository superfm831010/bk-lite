import os
import json

from apps.core.logger import monitor_logger as logger
from apps.monitor.services.plugin import MonitorPluginService


def find_json_paths(root_dir: str):
    """
    查找 plugins/type/config_type/variant/*.json 的文件路径。

    只要 path，忽略中间目录名和非 .json 文件。
    跳过任何不是目录的中间层。

    :param root_dir: 根目录路径，例如 'plugins'
    :return: 所有符合条件的 .json 文件完整路径列表
    """
    result = []
    for type_name in os.listdir(root_dir):
        type_path = os.path.join(root_dir, type_name)
        if not os.path.isdir(type_path):
            continue
        for config_name in os.listdir(type_path):
            config_path = os.path.join(type_path, config_name)
            if not os.path.isdir(config_path):
                continue
            for variant_name in os.listdir(config_path):
                variant_path = os.path.join(config_path, variant_name)
                if not os.path.isdir(variant_path):
                    continue
                for filename in os.listdir(variant_path):
                    if filename.endswith('.json'):
                        result.append(os.path.join(variant_path, filename))
    return result


def migrate_plugin():
    """迁移插件"""
    files_directory = 'apps/monitor/plugins'
    path_list = find_json_paths(files_directory)
    for file_path in path_list:
        # 打开并读取 JSON 文件
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                plugin_data = json.load(file)
                MonitorPluginService.import_monitor_plugin(plugin_data)
        except Exception as e:
            logger.error(f'导入插件 {file_path} 失败！原因：{e}')
