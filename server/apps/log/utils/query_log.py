import json

import requests
from apps.log.constants import VICTORIALOGS_HOST, VICTORIALOGS_USER, VICTORIALOGS_PWD, VICTORIALOGS_SSL_VERIFY


class VictoriaMetricsAPI:
    def __init__(self):
        self.host = VICTORIALOGS_HOST
        self.username = VICTORIALOGS_USER
        self.password = VICTORIALOGS_PWD
        self.ssl_verify = VICTORIALOGS_SSL_VERIFY

    def query(self, query, start, end, limit=10):
        data = {"query": query, "start": start, "end": end, "limit": limit}
        response = requests.post(
            f"{self.host}/select/logsql/query",
            params=data,
            auth=(self.username, self.password),
            verify=self.ssl_verify,  # 添加SSL验证配置
        )
        response.raise_for_status()
        result = []
        for line in response.text.strip().splitlines():
            if line:
                result.append(json.loads(line))
        return result

    def hits(self, query, start, end, field, fields_limit=5, step="5m"):
        data = {"query": query, "start": start, "end": end, "field": field, "fields_limit": fields_limit, "step": step}

        response = requests.post(
            f"{self.host}/select/logsql/hits",
            params=data,
            auth=(self.username, self.password),
            verify=self.ssl_verify,  # 添加SSL验证配置
        )
        response.raise_for_status()
        return response.json()

    def tail(self, query):
        # tail是一个长连接接口，用于实时获取日志数据
        data = {"query": query}
        with requests.post(
                f"{self.host}/select/logsql/tail",
                params=data,
                auth=(self.username, self.password),
                verify=self.ssl_verify,  # 添加SSL验证配置
                stream=True,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    yield line
