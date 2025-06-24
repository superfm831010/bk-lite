# -- coding: utf-8 --
# @File: base.py
# @Time: 2025/3/25 17:15
# @Author: windyzhao
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, timezone

import requests

from apps.cmdb.constants import VICTORIAMETRICS_HOST
from apps.cmdb.models import CollectModels
from apps.core.logger import cmdb_logger as logger


def timestamp_gt_one_day_ago(collect_timestamp):
    """
    判断时间戳是否大于一天前
    """
    # 获取当前时间
    current_time = datetime.now()
    # 计算一天前的时间
    one_day_ago = current_time - timedelta(days=1)
    # 转换为时间戳
    one_day_ago_timestamp = int(one_day_ago.timestamp())
    return collect_timestamp < one_day_ago_timestamp


# 采集数据（数据查询）
class Collection:
    def __init__(self):
        self.url = f"{VICTORIAMETRICS_HOST}/prometheus/api/v1/query"

    def query(self, sql, timeout=60):
        """查询数据"""
        resp = requests.post(self.url, data={"query": sql}, timeout=timeout)
        if resp.status_code != 200:
            raise Exception(f"request error！{resp.text}")
        return resp.json()


class CollectBase(metaclass=ABCMeta):
    """
     k8s、阿里云、vc 在vm对比后把旧数据自动删除，如果无数据，定义为这个采集任务异常，任务的数据清空，但是不碰cmdb的数据
    然后其他对象模型的采集，不删除数据
    """
    _MODEL_ID = None  # 模型ID，需要删除cmdb数据的采集子类需要定义 不定义不删除

    def __init__(self, inst_name, inst_id, task_id, *args, **kwargs):
        self.inst_id = inst_id
        self.task_id = task_id
        self.inst_name = inst_name
        assert self.check_metrics(), "请定义_metrics"
        self.collection_metrics_dict = {i: [] for i in self._metrics}
        self.timestamp_gt = False
        self.asso = "assos"
        self.result = {}

    @property
    @abstractmethod
    def _metrics(self):
        """指标名称"""
        raise NotImplementedError

    def check_metrics(self):
        return hasattr(self, "_metrics")

    @abstractmethod
    def format_data(self, data):
        """格式化数据"""
        raise NotImplementedError

    @abstractmethod
    def format_metrics(self):
        """格式化指标"""
        raise NotImplementedError

    @abstractmethod
    def prom_sql(self):
        """Prometheus查询语句"""
        raise NotImplementedError

    def get_collect_inst(self):
        instance = CollectModels.objects.get(id=self.task_id)
        return instance

    @property
    def model_id(self):
        instance = self.get_collect_inst()
        return instance.model_id

    def query_data(self):
        """查询数据"""
        sql = self.prom_sql()
        data = Collection().query(sql)
        return data.get("data", [])

    def run(self):
        """执行"""
        data = self.query_data()
        self.format_data(data)
        self.format_metrics()
        return self.result

    @staticmethod
    def convert_datetime_format(time_str):
        if not time_str:
            return ""
        try:
            # 解析为 datetime 对象
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            # 添加微秒并设置为 UTC 时区
            dt_utc = dt.replace(tzinfo=timezone.utc)
            # 转换为 ISO 8601 格式
            iso_format = dt_utc.isoformat()
        except Exception as err:
            logger.error("==Time Change Error! error={}==".format(err))
            iso_format = ""

        return iso_format
