import requests

from cmp import settings
from common.cmp.cloud_apis.resource_apis.resource_format.TKE_Cloud.tke_cloud_format import TKECloudResourceFormat


class CwTKECloud:
    """
    描述：TKE组件类
    修改记录: 2021-06-17 Amirhuang 创建
    """

    def __init__(self, **kwargs):
        """
        描述:初始化方法, 目前只需要一个token
        修改记录: 2021-06-17 Amirhuang 创建
        """
        pass

    def __getattr__(self, item):
        """
        描述:该魔术方法的妙用,当类没有item方法时,会执行该魔术方法,该魔术方法返回TKE类实例
        修改记录: 2021-06-17 Amirhuang 创建
        """
        return TKECloud(name=item)


class TKECloud:
    """
    描述：TKE相关方法的类
    修改记录: 2021-06-17 Amirhuang 创建
    """

    def __init__(self, name):
        """
        描述:初始化方法, 目前只需要一个token
        修改记录: 2021-06-17 Amirhuang 创建
        """
        self.name = name
        self.authorization = settings.TKE_TOKEN
        self.domain = settings.TKE_DOMAIN

    @classmethod
    def _non_function(cls, *args, **kwargs):
        return {"result": True, "data": []}

    def __call__(self, *args, **kwargs):
        return getattr(self, self.name, self._non_function)(*args, **kwargs)

    def node_details(self, name):
        """
        描述:查看节点详情,GET /apis/platform.tkestack.io/v1/machines/{name}
        修改记录: 2021-06-17 Amirhuang 创建
        """
        url = self.domain + "/apis/platform.tkestack.io/v1/machines/{}".format(name)
        headers = {"Authorization": self.authorization}
        response_data = requests.get(url, headers=headers).json()
        if not response_data:
            return []
        # print(TKECloudResourceFormat.format_node_list(response_data))
        return TKECloudResourceFormat.format_node_list(response_data)

    def node_list(self):
        """
        描述:查看节点列表,GET /apis/platform.tkestack.io/v1/machines
        修改记录: 2021-06-17 Amirhuang 创建
        """
        url = self.domain + "/apis/platform.tkestack.io/v1/machines"
        headers = {"Authorization": self.authorization}
        response_data = requests.get(url, headers=headers).json()
        if not response_data:
            return []
        node_lists = [TKECloudResourceFormat.format_node_list(item) for item in response_data["items"]]
        # print(node_lists)
        return node_lists

    def clusters(self):
        """
        描述:查看集群列表,GET /apis/platform.tkestack.io/v1/clusters
        修改记录: 2021-06-21 Amirhuang 创建
        """
        url = self.domain + "/apis/platform.tkestack.io/v1/clusters"
        headers = {"Authorization": self.authorization}
        response_data = requests.get(url, headers=headers).json()
        if not response_data:
            return []
        clusters = [TKECloudResourceFormat.format_clusters(item) for item in response_data["items"]]
        # print(clusters)
        return clusters

    def cluster_detail(self, name):
        """
        描述:查看集群详情,GET /apis/platform.tkestack.io/v1/clusters/{name}
        修改记录: 2021-06-21 Amirhuang 创建
        """
        url = self.domain + "/apis/platform.tkestack.io/v1/clusters/{}".format(name)
        headers = {"Authorization": self.authorization}
        response_data = requests.get(url, headers=headers).json()
        if not response_data:
            return []
        return TKECloudResourceFormat.format_clusters(response_data)

    def get_connection_result(self):
        """
        根据能否获取地域信息判断是否连接成功
        :return:
        """
        url = self.domain + "/apis/platform.tkestack.io/v1/machines"
        headers = {"Authorization": self.authorization}
        code = requests.get(url, headers=headers).status_code
        if code == 200:
            return {"result": "success"}
        else:
            return {"result": "failed"}


if __name__ == "__main__":
    pass
    # import os
    #
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    # import django
    #
    # django.setup()
    #
    # # cw = CwTKECloud()
    # # node_list = cw.node_list()
    # # print(node_list)
    # # cw.node_details('mc-6npmcrfm')
    # # cw.clusters()
    #
    # from common.cmp.cloud_apis.resource_apis.sync_cloud_resource.cloud_resource import SyncTKECloudResource
    #
    # sytke = SyncTKECloudResource()
    # sytke.sync_node_list()
