from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from django.db import models

from apps.log.models import CollectType


class Stream(TimeInfo, MaintainerInfo):
    id = models.CharField(primary_key=True, max_length=200, verbose_name='数据流ID')
    name = models.CharField(db_index=True, max_length=200, verbose_name='数据流名称')
    collect_type = models.ForeignKey(CollectType, null=True, blank=True, on_delete=models.CASCADE, verbose_name='采集方式')
    rule = models.JSONField(default=dict, verbose_name='规则')

    class Meta:
        verbose_name = "日志数据流"
        verbose_name_plural = '日志数据流'


class StreamOrganization(TimeInfo, MaintainerInfo):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, verbose_name='数据流')
    organization = models.IntegerField(verbose_name='组织ID')

    class Meta:
        verbose_name = '数据流组织'
        verbose_name_plural = '数据流组织'
        unique_together = ('stream', 'organization')
