import requests
from apps.log.constants import VICTORIAMETRICS_HOST, VICTORIAMETRICS_USER, VICTORIAMETRICS_PWD


class VictoriaMetricsAPI:
    def __init__(self):
        self.host = VICTORIAMETRICS_HOST
        self.username = VICTORIAMETRICS_USER
        self.password = VICTORIAMETRICS_PWD

    def query(self, query, start, end, limit=10):
        data = {"query": query, "start": start, "end": end, "limit": limit}
        response = requests.post(
            f"{self.host}/select/logsql/query",
            json=data,
            auth=(self.username, self.password),
        )
        response.raise_for_status()
        return response.json()

    def hits(self, query, start, end, field, fields_limit=5, step="5m"):
        data = {"query": query, "start": start, "end": end, "field": field, "fields_limit": fields_limit, "step": step}

        response = requests.post(
            f"{self.host}/select/logsql/hits",
            json=data,
            auth=(self.username, self.password),
        )
        response.raise_for_status()
        return response.json()
