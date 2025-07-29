import os
import uuid

from jinja2 import Environment, FileSystemLoader, DebugUndefined

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.log.models import CollectConfig, Stream
from apps.log.plugins import PLUGIN_DIRECTORY
from apps.log.utils.stream import StreamUtils
from apps.rpc.node_mgmt import NodeMgmt


class Controller:
    def __init__(self, data):
        self.data = data
        self.stream_rules = self.get_stream_rules()

    def get_stream_rules(self):
        streams = Stream.objects.filter(collect_type_id=self.data["collect_type_id"])
        stream_rules = []
        for stream in streams:
            stream_rules.append(
                {
                    "stream_id": stream.id,
                    "condition": StreamUtils.json_to_jq_expression(stream.rule),
                }
            )
        return stream_rules

    def get_template_info_by_type(self, template_dir: str, type_name: str):
        """
        从指定目录中查找匹配类型的 j2 模板文件，并解析出 type、config_type、file_type。

        :param template_dir: 模板文件所在目录
        :param type_name: 要查找的类型，例如 'cup'
        :return: 列表，每个元素是一个 dict，包含 type/config_type/file_type 三个字段
        """
        result = []
        for filename in os.listdir(template_dir):
            if not filename.endswith('.j2'):
                continue
            parts = filename[:-3].split('.')  # 去掉 .j2 后按 . 分割
            if len(parts) != 3:
                continue  # 忽略非法命名格式
            file_type, config_type, file_type_ext = parts
            if file_type != type_name:
                continue
            result.append({
                "type": file_type,
                "config_type": config_type,
                "file_type": file_type_ext
            })
        return result

    def render_template(self, template_dir: str, file_name: str, context: dict, stream_rules=None):
        """
        渲染指定目录下的 j2 模板文件。

        :param template_dir: 模板文件所在目录
        :param context: 用于模板渲染的变量字典
        :return: 渲染后的配置字符串
        """
        _context = {**context}
        _context.update(streams=stream_rules or [])
        env = Environment(loader=FileSystemLoader(template_dir), undefined=DebugUndefined)
        template = env.get_template(file_name)
        return template.render(_context)

    def format_configs(self):
        """ 格式化配置数据，将实例和配置合并成最终的配置列表。"""
        collect_type = self.data["collect_type"]
        collector = self.data["collector"]
        configs = []
        for instance in self.data["instances"]:
            node_ids = instance.pop("node_ids")
            for node_id in node_ids:
                node_info = {"node_id": node_id}
                for config in self.data["configs"]:
                    _config = {"collector": collector, "collect_type": collect_type, **node_info, **config, **instance}
                    configs.append(_config)
        return configs

    def controller(self):
        base_dir = PLUGIN_DIRECTORY
        configs = self.format_configs()
        node_configs, node_child_configs, collect_configs = [], [], []
        for config_info in configs:
            template_dir = os.path.join(base_dir, config_info["collector"], config_info["collect_type"])
            templates = self.get_template_info_by_type(template_dir, config_info["collect_type"])
            env_config = {k[4:]: v for k, v in config_info.items() if k.startswith("ENV_")}
            for template in templates:
                is_child = True if template["config_type"] == "child" else False
                collector_name = "Vector" if is_child else config_info["collector"]
                config_id = str(uuid.uuid4().hex)
                # 生成配置
                template_config = self.render_template(
                    template_dir,
                    f"{template['type']}.{template['config_type']}.{template['file_type']}.j2",
                    config_info,
                    self.stream_rules
                )

                # 节点管理创建配置
                if is_child:
                    node_child_config = dict(
                        id=config_id,
                        collect_type=config_info["collect_type"],
                        type=config_info["collect_type"],
                        content=template_config,
                        node_id=config_info["node_id"],
                        collector_name=collector_name,
                        env_config=env_config,
                    )
                    node_child_configs.append(node_child_config)
                else:
                    node_config = dict(
                        id=config_id,
                        name=f'{collector_name}-{config_id}',
                        content=template_config,
                        node_id=config_info["node_id"],
                        collector_name=collector_name,
                        env_config=env_config,
                    )
                    node_configs.append(node_config)

                # 监控记录配置
                collect_configs.append(
                    CollectConfig(
                        id=config_id,
                        collect_instance_id=config_info["instance_id"],
                        file_type=template["file_type"],
                        is_child=is_child,
                    )
                )

        # 记录实例与配置的关系
        CollectConfig.objects.bulk_create(collect_configs, batch_size=100)
        # 创建配置
        NodeMgmt().batch_add_node_config(node_configs)
        # 创建子配置
        NodeMgmt().batch_add_node_child_config(node_child_configs)

    def render_config_template_content(self, file_type, context_data):
        """ 渲染配置模板内容。"""

        template_dir = os.path.join(PLUGIN_DIRECTORY, self.data["collector"], self.data["collect_type"])
        templates = self.get_template_info_by_type(template_dir, self.data["collect_type"])

        template = None

        for _template in templates:
            if _template["config_type"] != file_type:
                continue
            template = _template

        if template is None:
            raise BaseAppException(f"No matching template found for {self.data['collect_type']} with file type {file_type}")

        # 生成配置
        content = self.render_template(
            template_dir,
            f"{template['type']}.{template['config_type']}.{template['file_type']}.j2",
            context_data,
            self.stream_rules
        )

        return content