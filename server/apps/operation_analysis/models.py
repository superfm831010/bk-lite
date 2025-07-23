# -- coding: utf-8 --
# @File: models.py
# @Time: 2025/7/14 16:03
# @Author: windyzhao
from django.db import models
from django.db.models import JSONField

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class DataSourceAPIModel(MaintainerInfo, TimeInfo):
    name = models.CharField(max_length=255, verbose_name="数据源名称", unique=True)
    rest_api = models.CharField(max_length=255, verbose_name="REST API URL", unique=True)
    desc = models.TextField(verbose_name="描述", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    params = JSONField(help_text="API请求参数", verbose_name="请求参数", blank=True, null=True)

    class Meta:
        db_table = "operation_analysis_data_source_api"
        verbose_name = "数据源API"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]


