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


    class Meta:
        verbose_name = "rasa规则"
        verbose_name_plural = "rasa规则"

    def __str__(self):
        return f'{self.name}-{self.dataset.name}'

