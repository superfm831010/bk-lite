from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.rasa_dataset import RasaDatasets

class RasaAction(MaintainerInfo, TimeInfo):
    "Rasa对话机器人Action"

    name = models.CharField(max_length=100,verbose_name="Action名称",unique=True)

    dataset = models.ForeignKey(
        RasaDatasets,
        on_delete=models.CASCADE,
        related_name="actions",
        verbose_name="数据集"
    )
    
    class Meta:
        verbose_name = "Rasa对话机器人Action"
        verbose_name_plural = "Rasa对话机器人Actions"

    def __str__(self):
        return f'{self.name}-{self.dataset.name}'
