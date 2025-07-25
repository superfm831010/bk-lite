# -- coding: utf-8 --
# @File: alerts.py
# @Time: 2025/7/22 18:29
# @Author: windyzhao

from apps.rpc.base import RpcClient


class Alert(object):
    def __init__(self):
        self.client = RpcClient()

    def get_alert_trend_data(self, group_by, filters):
        """
        :param group_by: 分组方式
        :param filters: 过滤条件，字典格式
        :return: 告警趋势数据
        """
        return_data = self.client.run("get_alert_trend_data", group_by, filters)
        return return_data
