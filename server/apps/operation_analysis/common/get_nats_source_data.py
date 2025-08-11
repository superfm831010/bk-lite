# -- coding: utf-8 --
# @File: get_nats_source_data.py
# @Time: 2025/7/22 18:24
# @Author: windyzhao
from apps.rpc.alerts import AlertOperationAna
from apps.core.logger import operation_analysis_logger as logger


class GetNatsData:
    """
    获取NATS数据源数据
    """

    def __init__(self, namespace: str, path: str, namespace_list: list, params: dict = None):
        self.path = path
        self.params = params or {}
        self.namespace = namespace
        self.namespace_list = namespace_list
        self.namespace_server_map = self.set_namespace_servers()
        self.namespace_map = self.set_namespace_map()

    def set_namespace_servers(self):
        result = {}
        for namespace in self.namespace_list:
            if ':' not in namespace.domain:
                server_url = f"nats://{namespace.account}:{namespace.decrypt_password}@{namespace.domain}:4222"
            else:
                server_url = f"nats://{namespace.account}:{namespace.decrypt_password}@{namespace.domain}"

            result[namespace.id] = server_url
        return result

    @staticmethod
    def set_namespace_map():
        # TODO 每个注册的命名空间 必须重写__init__ 补上server参数
        result = {"alert": AlertOperationAna}
        return result

    def _get_client(self, server):
        if self.namespace not in self.namespace_map.keys():
            raise Exception("NATS namespace not found")

        client = self.namespace_map[self.namespace](server=server)
        return client

    def get_data(self):
        """
        获取NATS数据源数据
        :return: 数据内容
        TODO 如果速度过慢，可以考虑使用多线程或异步方式来并发获取数据
        """
        result = {}
        for namespace in self.namespace_list:
            server_url = self.namespace_server_map[namespace.id]
            nats_client = self._get_client(server=server_url)
            try:
                fun = getattr(nats_client, self.path, None)
                if fun is None:
                    raise RuntimeError(f"NamePaces({self.namespace}) Module not found func({self.path})!")

                return_data = fun(**self.params)
                result[namespace.id] = return_data
            except Exception as e:
                result[namespace.name] = {}
                import traceback
                logger.error(
                    "==获取NATS数据源数据失败==: namespace={} error={}".format(namespace.name, traceback.format_exc()))

        return result
