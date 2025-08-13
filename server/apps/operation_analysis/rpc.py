# -- coding: utf-8 --
# @File: rpc.py
# @Time: 2025/8/11 10:41
# @Author: windyzhao
import asyncio

import nats_client
from apps.rpc.base import RpcClient


# from apps.core.logger import operation_analysis_logger as logger


class OperationAnalysisRpc(RpcClient):
    """
    操作分析专用RPC客户端
    支持自定义服务器地址，独立于框架基础RpcClient实现
    """

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop("namespace", None)
        super().__init__(namespace=self.namespace)
        self.server = kwargs.pop("server", "")

    def run(self, method_name, *args, **kwargs):
        return_data = asyncio.run(
            nats_client.request_v2(self.namespace, method_name, server=self.server, *args, **kwargs))
        return return_data
