from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.rasa_dataset import RasaDatasets


class RasaPipeline(MaintainerInfo, TimeInfo):
    """Rasa训练管道模型"""

    name = models.CharField(max_length=100, verbose_name="管道名称", unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="管道描述")
    
    # JSON配置字段，用于存储Rasa pipeline配置
    config = models.JSONField(
        verbose_name="管道配置",
        default=dict,
        help_text="Rasa pipeline配置，包含tokenizer、featurizer、classifier等组件"
    )
    
    # 关联多个数据集，一个pipeline可以关联多个dataset
    datasets = models.ManyToManyField(
        RasaDatasets,
        related_name="pipelines",
        verbose_name="关联数据集",
        blank=True,
        help_text="该管道关联的训练数据集"
    )

    class Meta:
        verbose_name = "Rasa训练管道"
        verbose_name_plural = "Rasa训练管道"

    def __str__(self):
        return self.name

    def get_dataset_count(self):
        """获取关联的数据集数量"""
        return self.datasets.count()

    def get_dataset_names(self):
        """获取关联的数据集名称列表"""
        return list(self.datasets.values_list('name', flat=True))