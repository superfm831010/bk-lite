from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.rasa_dataset import RasaDatasets

class RasaResponse(MaintainerInfo, TimeInfo):

    name = models.CharField(max_length=100, verbose_name="响应名称", unique=True)

    dataset = models.ForeignKey(
        RasaDatasets,
        on_delete=models.CASCADE,
        related_name="responses",
        verbose_name="数据集"
    )

    example = models.JSONField(
        verbose_name="响应示例",
        default=list
    )

    example_count = models.IntegerField(
        default=0,
        verbose_name="响应示例数量"
    )

    class Meta:
        verbose_name = "rasa响应"
        verbose_name_plural = "rasa响应"

    def __str__(self):
        return f'{self.name}-{self.dataset.name}'

    def save(self, *args, **kwargs):
        """
        保存时自动计算样例个数
        """
        if isinstance(self.example, list):
            self.example_count = len(self.example)
        else:
            self.example_count = 0
        super().save(*args, **kwargs)