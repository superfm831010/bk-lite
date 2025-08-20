# apps/mlops/models/rasa_entity.py
from django.db import models
from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.rasa_dataset import RasaDatasets


class RasaEntity(MaintainerInfo, TimeInfo):
    """
    Rasa 实体模型
    用于管理对话系统中的实体信息
    """

    ENTITY_TYPES = [
        ('Text', '自由标注'),
        ('Lookup', '枚举表'),
        # 可以根据需要添加更多类型
    ]

    name = models.CharField(max_length=100, verbose_name="实体名称", unique=True)
    dataset = models.ForeignKey(
        RasaDatasets,
        on_delete=models.CASCADE,
        related_name="entities",
        verbose_name="数据集"
    )

    entity_type = models.CharField(
        max_length=20,
        choices=ENTITY_TYPES,
        verbose_name="类型",
        default='Text'
    )

    # 存储实体值的列表
    example = models.JSONField(
        verbose_name="实体值",
        default=list,
        help_text="实体的具体取值列表"
    )

    # 可选：描述字段
    description = models.TextField(blank=True, null=True, verbose_name="描述")

    class Meta:
        verbose_name = "实体"
        verbose_name_plural = "实体"

    def __str__(self):
        return f'{self.name}-{self.dataset.name}'
