from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class CollectType(TimeInfo, MaintainerInfo):

    name = models.CharField(max_length=100, verbose_name='采集方式')
    collector = models.CharField(max_length=100, verbose_name='采集器')
    icon = models.CharField(max_length=100, verbose_name='图标')
    description = models.TextField(blank=True, verbose_name='描述')

    class Meta:
        verbose_name = '采集方式'
        verbose_name_plural = '采集方式'
        unique_together = ('name', 'collector')


class CollectInstance(TimeInfo, MaintainerInfo):
    id = models.CharField(primary_key=True, max_length=200, verbose_name='采集方式实例ID')
    name = models.CharField(db_index=True, max_length=200, verbose_name='采集方式实例名称')
    collect_type = models.ForeignKey(CollectType, on_delete=models.CASCADE, verbose_name='采集方式')

    class Meta:
        verbose_name = '采集方式实例'
        verbose_name_plural = '采集方式实例'


class CollectInstanceOrganization(TimeInfo, MaintainerInfo):
    collect_instance = models.ForeignKey(CollectInstance, on_delete=models.CASCADE, verbose_name='监控对象实例')
    organization = models.CharField(max_length=100, verbose_name='组织id')

    class Meta:
        verbose_name = '采集方式实例组织'
        verbose_name_plural = '采集方式实例组织'
        unique_together = ('collect_instance', 'organization')


class CollectConfig(TimeInfo, MaintainerInfo):
    id = models.CharField(primary_key=True, max_length=100, verbose_name='配置ID')
    collect_instance = models.ForeignKey(CollectInstance, on_delete=models.CASCADE, verbose_name='采集方式实例')
    file_type = models.CharField(max_length=50, verbose_name='文件类型')
    is_child = models.BooleanField(default=False, verbose_name='是否子配置')

    class Meta:
        verbose_name = '采集配置'
        verbose_name_plural = '采集配置'
