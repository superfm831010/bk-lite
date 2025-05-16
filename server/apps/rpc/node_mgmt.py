from apps.rpc.base import RpcClient


class NodeMgmt(object):
    def __init__(self):
        self.client = RpcClient('node_mgmt')

    def cloud_region_list(self):
        """
        :return: 云区域列表
        """
        return_data = self.client.run('cloud_region_list')
        return return_data

    def node_list(self, query_data):
        """
        :param query_data: 查询条件
        {
            "cloud_region_id": 1,
            "organization_ids": ["1", "2"],
            "name": "node_name",
            "ip": "10.10.10.1",
            "os": "linux/windows",
            "page": 1,
            "page_size": 10,
        }
        """
        return_data = self.client.run('node_list', query_data)
        return return_data

    def batch_add_node_child_config(self, data):
        """
        适用子配置的采集器枚举 ["Telegraf"]
        :param data: 批量添加配置（以下为一个http prometheus的采集参数）
        {
            "collector": "Telegraf",   // 收集器名称
            "nodes": [{                     // 节点列表
                "id": "27439797-fd14-4e18-b54e-3f7ce8727030",
                "configs": [{
                    # 通用参数
                    "id": "uuid", // 配置id，调用方自己生成
                    "collect_type": "http", // 采集方式
                    "type": "prometheus", // 配置类型
                    "interval": "", // 采集间隔
                    "instance_id": "",      // 实例ID
                    "instance_type": "",    // 实例类型
                    # 采集器模版参数，不同采集器不同
                    "url": "",
                    "timeout": "",
                    "response_timeout": "",
                    "custom_headers": "",
                }]
            }]
        }
        """
        return_data = self.client.run('batch_add_node_child_config', data)
        return return_data

    def batch_add_node_config(self, data):
        """
        适用配置的采集器枚举 ["JMX-JVM"]
        :param data: 批量添加配置（以下为一个jmx jvm的采集参数）
        {
            "collector": "JMX-JVM",   // 收集器名称
            "nodes": [{                     // 节点列表
                "id": "27439797-fd14-4e18-b54e-3f7ce8727030",
                "configs": [{
                    # 通用参数
                    "id": "uuid", // 配置id，调用方自己生成
                    "collect_type": "jmx", // 采集方式
                    "type": "jvm", // 配置类型
                    # 采集器模版参数，不同采集器不同
                    "username": "",
                    "password": "",
                    "jmx_url": "",
                }]
            }]
        }
        """
        return_data = self.client.run('batch_add_node_config', data)
        return return_data

    def get_child_configs_by_ids(self, ids):
        """
        :param ids: 子配置ID列表
        """
        return_data = self.client.run('get_child_configs_by_ids', ids)
        return return_data

    def get_configs_by_ids(self, ids):
        """
        :param ids: 配置ID列表
        """
        return_data = self.client.run('get_configs_by_ids', ids)
        return return_data

    def update_child_config_content(self, id, content):
        """
        :param id: 子配置ID
        :param content: 子配置内容
        """
        return_data = self.client.run('update_child_config_content', {"id": id, "content": content})
        return return_data

    def update_config_content(self, id, content):
        """
        :param id: 配置ID
        :param content: 配置内容
        """
        return_data = self.client.run('update_config_content', {"id": id, "content": content})
        return return_data

    def delete_child_configs(self, ids):
        """
        :param ids: 子配置ID列表
        """
        return_data = self.client.run('delete_child_configs', ids)
        return return_data

    def delete_configs(self, ids):
        """
        :param ids: 配置ID列表
        """
        return_data = self.client.run('delete_configs', ids)
        return return_data
