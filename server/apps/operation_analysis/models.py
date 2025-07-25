# -- coding: utf-8 --
# @File: models.py
# @Time: 2025/7/14 16:03
# @Author: windyzhao
from django.db import models
from django.db.models import JSONField

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.operation_analysis.constants import DashboardType


class DataSourceAPIModel(MaintainerInfo, TimeInfo):
    name = models.CharField(max_length=255, verbose_name="数据源名称")
    rest_api = models.CharField(max_length=255, verbose_name="REST API URL")
    desc = models.TextField(verbose_name="描述", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    params = JSONField(help_text="API请求参数", verbose_name="请求参数", blank=True, null=True)

    class Meta:
        db_table = "operation_analysis_data_source_api"
        verbose_name = "数据源API"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'rest_api'],
                name='unique_name_rest_api'
            ),
        ]


class Dashboard(MaintainerInfo, TimeInfo):
    name = models.CharField(max_length=128, verbose_name="仪表盘名称")
    type = models.CharField(max_length=64, verbose_name="仪表盘类型", choices=DashboardType.CHOICES)
    data_source = models.ForeignKey(
        DataSourceAPIModel, on_delete=models.CASCADE, related_name="dashboards", verbose_name="数据源"
    )
    filters = JSONField(help_text="仪表盘过滤条件", verbose_name="过滤条件", blank=True, null=True)
    other = JSONField(help_text="其他配置", verbose_name="其他配置", blank=True, null=True)

    class Meta:
        db_table = "operation_analysis_dashboard"
        verbose_name = "仪表盘"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_name_type'
            ),
        ]
