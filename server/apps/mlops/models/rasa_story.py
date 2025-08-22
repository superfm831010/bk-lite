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

    intent_count = models.IntegerField(
        default=0,
        verbose_name="意图数量"
    )

    response_count = models.IntegerField(
        default=0,
        verbose_name="响应数量"
    )

    def __str__(self):
        return f'{self.name}-{self.dataset.name}'

    def save(self, *args, **kwargs):
        if isinstance(self.steps, list):
            self.intent_count = int(len([i for i in self.steps if 'intent' in i]))
            self.response_count = int(len([i for i in self.steps if 'response' in i]))
        else:
            self.intent_count = 0
            self.response_count = 0
        super().save(*args, **kwargs)
