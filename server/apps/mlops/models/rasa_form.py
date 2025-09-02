from django.db import models
from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.rasa_dataset import RasaDatasets

class RasaForm(MaintainerInfo, TimeInfo):

    name = models.CharField(max_length=100, verbose_name="表单名称", unique=True)

    dataset = models.ForeignKey(
        RasaDatasets,
        on_delete=models.CASCADE,
        related_name="forms",
        verbose_name="数据集"
    )

    slots = models.JSONField(
        verbose_name="表单字段",
        default=list,
        help_text="表单字段列表"
    )

    class Meta:
        verbose_name = "表单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}-{self.dataset.name}'