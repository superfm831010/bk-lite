# -- coding: utf-8 --
# @File: alerts.py
# @Time: 2025/7/22 18:29
# @Author: windyzhao
from apps.operation_analysis.rpc import OperationAnalysisRpc


class AlertOperationAna(object):
    def __init__(self, *args, **kwargs):
        params = {}
        server = kwargs.get("server", None)
        if server:
            params["server"] = server
        self.client = OperationAnalysisRpc(**params)

    def get_alert_trend_data(self, *args, **kwargs):
        """
        :param group_by: 分组方式
        :param filters: 过滤条件，字典格式
        :return: 告警趋势数据
        """
        return_data = self.client.run("get_alert_trend_data", *args, **kwargs)
        return return_data
