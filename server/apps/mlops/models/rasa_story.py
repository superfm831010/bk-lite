from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.rasa_dataset import RasaDatasets

class RasaStory(MaintainerInfo, TimeInfo):
    """
    rasa故事训练数据
    """

    name = models.CharField(max_length=100, verbose_name="故事名称", unique=True)

    dataset = models.ForeignKey(
        RasaDatasets,
        on_delete=models.CASCADE,
        related_name="stories",
        verbose_name="数据集"
    )

    steps = models.JSONField(
        verbose_name="故事步骤",
        default=list
    )


    def __str__(self):
        return f'{self.name}-{self.dataset.name}'

