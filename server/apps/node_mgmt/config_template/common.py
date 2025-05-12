import ast
import os
import re
from jinja2 import Environment, FileSystemLoader

from apps.node_mgmt.models import CollectorConfiguration, ChildConfig, Collector, Node, NodeCollectorConfiguration


# key为采集器名称, value为采集器模版目录，只维护采集类的采集器
COLLECTOR_PATH_MAP = {
    "Telegraf": "telegraf",
    "JMX-JVM": "exporter",
}


class ConfigService:
    def __init__(self):
        self.template_root = "apps/node_mgmt/config_template"

    def render_config(self, subdir: str, collect_method: str, target: str, context: dict) -> str:
        """
        渲染配置文件
        :param subdir: 子目录（如 "telegraf", "exporter"）
        :param collect_method: 采集方式目录（如 "jmx"）
        :param target: 采集对象（如 "jvm"）
        :param context: 用于模板渲染的变量字典
        :return: 渲染后的配置字符串
        """
        target_dir = os.path.join(self.template_root, subdir, collect_method)
        if not os.path.isdir(target_dir):
            raise FileNotFoundError(f"Template dir '{target_dir}' not found.")

        # 文件名格式：target.文件类型.j2，例如 jvm.yaml.j2
        pattern = rf"^{re.escape(target)}\.\w+\.j2$"

        for filename in os.listdir(target_dir):
            if re.match(pattern, filename):
                env = Environment(loader=FileSystemLoader(target_dir))
                template = env.get_template(filename)
                return template.render(context)

        raise FileNotFoundError(f"No template matching '{target}.*.j2' in '{target_dir}'")

    def batch_add_child_config(self, collector, nodes: list):
        """批量添加子配置"""
        subdir = f"config/{COLLECTOR_PATH_MAP.get(collector)}"
        node_objs, base_config_ids = [], []
        for node in nodes:
            node_id = node["id"]
            node_configs = node["configs"]
            base_config = CollectorConfiguration.objects.filter(nodes__id=node_id, collector__name=collector).first()
            base_config_id = base_config.id
            base_config_ids.append(base_config_id)
            for node_config in node_configs:

                node_config["instance_id"] = ast.literal_eval(node_config["instance_id"])[0]
                content = self.render_config(subdir, node_config["collect_type"], node_config["type"], node_config)

                node_objs.append(ChildConfig(
                    id=node_config["id"],
                    collect_type=node_config["collect_type"],
                    config_type=node_config["type"],
                    content=content,
                    collector_config_id=base_config_id,
                ))
        if node_objs:
            ChildConfig.objects.bulk_create(node_objs, batch_size=100)

    def batch_add_config(self, collector, nodes: list):
        """批量添加配置"""
        collector_objs = Collector.objects.filter(name=collector)
        if not collector_objs:
            raise ValueError(f"Collector '{collector}' not found")
        collector_map = {obj.node_operating_system: obj for obj in collector_objs}
        subdir = f"config/{COLLECTOR_PATH_MAP.get(collector)}"

        conf_objs = []
        node_config_assos = []
        for node in nodes:
            node_id = node["id"]
            node_configs = node["configs"]

            node_obj = Node.objects.filter(id=node_id).values("cloud_region_id", "operating_system").first()
            if not node_obj:
                raise ValueError(f"Node '{node_id}' not found")
            cloud_region_id = node_obj["cloud_region_id"]
            os = node_obj["operating_system"]
            collector_obj = collector_map.get(os)

            for node_config in node_configs:

                node_config["instance_id"] = ast.literal_eval(node_config["instance_id"])[0]
                content = self.render_config(subdir, node_config["collect_type"], node_config["type"], node_config)

                conf_objs.append(CollectorConfiguration(
                    id=node_config["id"],
                    name=f"{collector}-{node_config['id']}",
                    config_template=content,
                    collector_id=collector_obj.id,
                    cloud_region_id=cloud_region_id,

                ))
                node_config_assos.append(NodeCollectorConfiguration(node_id=node_id, collector_config_id=node_config["id"]))

        if conf_objs:
            CollectorConfiguration.objects.bulk_create(conf_objs, batch_size=100)
        if node_config_assos:
            NodeCollectorConfiguration.objects.bulk_create(node_config_assos, batch_size=100, ignore_conflicts=True)

    def get_child_configs_by_ids(self, ids: list):
        """根据子配置ID列表获取子配置对象"""
        child_configs = ChildConfig.objects.filter(id__in=ids)
        return [
            {
                "id": config.id,
                "collect_type": config.collect_type,
                "config_type": config.config_type,
                "content": config.content,
            }
            for config in child_configs
        ]

    def get_configs_by_ids(self, ids: list):
        """根据配置ID列表获取配置对象"""
        configs = CollectorConfiguration.objects.filter(id__in=ids)

        return [
            {
                "id": config.id,
                "name": config.name,
                "config_template": config.config_template,
            }
            for config in configs
        ]

    def update_child_config_content(self, id, content):
        """更新子配置内容"""
        child_config = ChildConfig.objects.filter(id=id).first()
        if child_config:
            child_config.content = content
            child_config.save()
        else:
            raise ValueError(f"ChildConfig with id {id} does not exist.")

    def update_config_content(self, id, content):
        """更新配置内容"""
        config = CollectorConfiguration.objects.filter(id=id).first()
        if config:
            config.config_template = content
            config.save()
        else:
            raise ValueError(f"CollectorConfiguration with id {id} does not exist.")

    def delete_child_configs(self, ids):
        """删除子配置"""
        ChildConfig.objects.filter(id__in=ids).delete()

    def delete_configs(self, ids):
        """删除配置"""
        CollectorConfiguration.objects.filter(id__in=ids).delete()
