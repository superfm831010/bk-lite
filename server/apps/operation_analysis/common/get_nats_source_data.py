# -- coding: utf-8 --
# @File: get_nats_source_data.py
# @Time: 2025/7/22 18:24
# @Author: windyzhao

class GetNatsData:
    """
    获取NATS数据源数据
    """

    def __init__(self, namespace: str, path: str, params: dict = dict):
        self.path = path
        self.params = params
        self.namespace = namespace
        self.namespace_map = self.set_namespace_map()
        self.nats_client = self._get_client()

    @staticmethod
    def set_namespace_map():
        from apps.rpc.alerts import Alert
        from apps.rpc.cmdb import CMDB
        result = {"alert": Alert, "cmdb": CMDB}
        return result

    def _get_client(self):
        if self.namespace not in self.namespace_map.keys():
            raise Exception("NATS namespace not found")

        client = self.namespace_map[self.namespace]()
        return client

    def get_data(self):
        """
        获取NATS数据源数据
        :return: 数据内容
        """
        try:
            fun = getattr(self.nats_client, self.path, None)
            if fun is None:
                raise RuntimeError(f"NamePaces({self.namespace}) Module not found func({self.path})!")

            return_data = fun(**self.params)
            return return_data
        except Exception as e:
            raise RuntimeError(f"获取NATS数据源数据失败: {e}")
