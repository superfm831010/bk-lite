from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.rasa_dataset import RasaDatasets

class RasaSlot(MaintainerInfo, TimeInfo):
    """槽位模型"""
    name = models.CharField(max_length=100, verbose_name="槽位名称", unique=True)

    dataset = models.ForeignKey(
        RasaDatasets,
        on_delete=models.CASCADE,
        related_name="slots",
        verbose_name="数据集"
    )

    SLOT_TYPE = [
        ('Text', '记录普通文本'),
        ('Categorical', '记录分类类别，枚举'),
        ('Float', '记录数值'),
        ('Bool', '记录布尔值'),
        ('List', '记录数值列表'),
    ]

    solt_type = models.CharField(
        max_length=20,
        choices=SLOT_TYPE,
        verbose_name="槽位类型",
        default='Text'
    )

    is_apply = models.BooleanField(
        default=False,
        verbose_name="是否应用"
    )

    class Meta:
        verbose_name = "槽位"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}-{self.dataset.name}'