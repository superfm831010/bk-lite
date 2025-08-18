from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.rasa_dataset import RasaDatasets

class RasaRule(MaintainerInfo, TimeInfo):

    name = models.CharField(max_length=100, verbose_name="规则名称", unique=True)

    dataset = models.ForeignKey(
        RasaDatasets,
        on_delete=models.CASCADE,
        related_name="rules",
        verbose_name="数据集"
    )

    steps = models.JSONField(
        verbose_name="规则步骤",
        default=list
    )

    intent_count = models.IntegerField(
        default=0,
        verbose_name="意图数量"
    )

    response_count = models.IntegerField(
        default=0,
        verbose_name="响应数量"
    )

    class Meta:
        verbose_name = "rasa规则"
        verbose_name_plural = "rasa规则"

    def __str__(self):
        return f'{self.name}-{self.dataset.name}'

    def save(self, *args, **kwargs):
        """
        重写save方法，保存时自动计算count
        """
        if isinstance(self.steps,list):
            self.intent_count = int(len([i for i in self.steps if 'intent' in i]))
            self.response_count = int(len([i for i in self.steps if 'response' in i]))
        else:
            self.intent_count = 0
            self.response_count = 0
        super().save(*args, **kwargs)