import uuid

from apps.monitor.collect_config.constants import ONLY_CHILD_CONFIG, CONFIG_AND_CHILD_CONFIG, ONLY_CONFIG
from apps.monitor.constants import CHILD_ENVS
from apps.monitor.models import CollectConfig
from apps.rpc.node_mgmt import NodeMgmt




class Controller:
    def __init__(self, data):
        self.data = data

    def set_config_id(self, config):
        config.update(id=str(uuid.uuid4().hex))

    def format_child_config(self, config):
        if config['collect_type'] == "snmp":
            self.format_snmp_config(config)
        elif config['collect_type'] == "http":
            self.format_http_config(config)

    def format_snmp_config(self, config):
        if config["version"] == 2:
            result = dict(
                agents=[f"udp://{config['ip']}:{config['port']}"],
                version=2,
                community=config["community"],
                timeout=config["timeout"],
            )
        elif config["version"] == 3:
            result = dict(
                agents=[f"udp://{config['ip']}:{config['port']}"],
                version=3,
                timeout=config["timeout"],
                sec_name=config["sec_name"],
                sec_level=config["sec_level"],
                auth_protocol=config["auth_protocol"],
                auth_password=config["auth_password"],
                priv_protocol=config["priv_protocol"],
                priv_password=config["priv_password"],
            )
        else:
            raise ValueError("SNMP version error")
        config.update(snmp_config=result)

    def format_http_config(self, config):
        url = f"${{STARGAZER_URL}}/api/monitor/{config['instance_type']}/metrics"
        config.update(url=url)
        if config["instance_type"] == "vmware":
            config["custom_headers"].update(host=config["host"])

    def only_child_config(self):

        file_type = ONLY_CHILD_CONFIG.get((self.data["collector"], self.data["collect_type"]))

        collect_type = self.data["collect_type"]
        configs = self.data["configs"]
        instances = self.data["instances"]
        collector = self.data["collector"]
        result = {
            "collector": collector,
            "nodes": [],
        }
        config_objs = []

        for instance in instances:
            node_ids = instance.pop("node_ids")
            for node_id in node_ids:
                node_info = {"id": node_id, "configs": []}
                for config in configs:
                    config_info = {"collect_type": collect_type, **config, **instance}

                    self.set_config_id(config_info)
                    self.format_child_config(config_info)

                    node_info["configs"].append(config_info)
                    config_objs.append(
                        CollectConfig(
                            id=config_info["id"],
                            collector=collector,
                            monitor_instance_id=instance["instance_id"],
                            collect_type=collect_type,
                            config_type=config["type"],
                            file_type=file_type,
                        )
                    )
                result["nodes"].append(node_info)

        # 记录实例与配置的关系
        CollectConfig.objects.bulk_create(config_objs, batch_size=100)
        # 创建配置
        NodeMgmt().batch_add_node_child_config(result)

    def only_config(self):
        pass

    def config_and_child_config(self):
        file_type = CONFIG_AND_CHILD_CONFIG.get((self.data["collector"], self.data["collect_type"]))
        child_file_type = ONLY_CHILD_CONFIG.get(("Telegraf", self.data["collect_type"]))

        collect_type = self.data["collect_type"]
        configs = self.data["configs"]
        instances = self.data["instances"]
        collector = self.data["collector"]
        config_result = {
            "collector": collector,
            "nodes": [],
        }
        child_config_result = {
            "collector": "Telegraf",
            "nodes": [],
        }
        config_objs, child_config_objs  = [], []

        for instance in instances:
            node_ids = instance.pop("node_ids")
            for node_id in node_ids:
                node_info = {"id": node_id, "configs": []}
                child_node_info = {"id": node_id, "configs": []}
                for config in configs:
                    config_info = {"collect_type": collect_type, **config, **instance}
                    self.set_config_id(config_info)
                    node_info["configs"].append(config_info)

                    child_config_info = {
                        "instance_id": config_info.get("instance_id"),
                        "instance_type":config_info.get("instance_type"),
                        "collect_type": collect_type,
                        "type": config_info.get("type"),
                        "interval": config_info.get("interval", 10),
                    }

                    # 共享变量同步到子配置
                    for k, v in config_info.items():
                        if k in CHILD_ENVS:
                            child_config_info[k] = v

                    self.set_config_id(child_config_info)
                    child_node_info["configs"].append(child_config_info)

                    config_result["nodes"].append(node_info)
                    child_config_result["nodes"].append(child_node_info)

                    config_objs.append(
                        CollectConfig(
                            id=config_info["id"],
                            collector=collector,
                            monitor_instance_id=instance["instance_id"],
                            collect_type=collect_type,
                            config_type=config["type"],
                            file_type=file_type,
                            is_child=False,
                        )
                    )
                    child_config_objs.append(
                        CollectConfig(
                            id=child_config_info["id"],
                            collector="Telegraf",
                            monitor_instance_id=instance["instance_id"],
                            collect_type=collect_type,
                            config_type=config["type"],
                            file_type=child_file_type,
                            is_child=True,
                        )
                    )

        # 记录实例与配置的关系
        CollectConfig.objects.bulk_create(config_objs, batch_size=100)
        # 创建配置
        NodeMgmt().batch_add_node_config(config_result)

        # 记录实例与子配置的关系
        CollectConfig.objects.bulk_create(child_config_objs, batch_size=100)
        # 创建子配置
        NodeMgmt().batch_add_node_child_config(child_config_result)

    def main(self):
        collect_type = self.data["collect_type"]
        collector = self.data["collector"]
        if (collector, collect_type) in ONLY_CHILD_CONFIG:
            self.only_child_config()
        elif (collector, collect_type) in ONLY_CONFIG:
            self.only_config()
        elif (collector, collect_type) in CONFIG_AND_CHILD_CONFIG:
            self.config_and_child_config()
        else:
            raise ValueError("Unsupported collector or collect type")
