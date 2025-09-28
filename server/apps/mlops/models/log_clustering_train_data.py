from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.log_clustering_dataset import LogClusteringDataset


class LogClusteringTrainData(MaintainerInfo, TimeInfo):
    """日志聚类训练数据模型"""

    name = models.CharField(max_length=100, verbose_name="训练数据名称")
    
    dataset = models.ForeignKey(
        LogClusteringDataset,
        on_delete=models.CASCADE,
        related_name="train_data",
        verbose_name="数据集",
    )
    
    train_data = models.JSONField(
        verbose_name="训练数据",
        help_text="存储日志聚类训练数据",
    )
    
    metadata = models.JSONField(
        verbose_name="元数据",
        blank=True,
        null=True,
        help_text="训练数据元信息",
    )

    is_train_data = models.BooleanField(
        default=False,
        verbose_name="是否为训练数据",
        help_text="是否为训练数据"
    )

    is_val_data = models.BooleanField(
        default=False,
        verbose_name="是否为验证数据",
        help_text="是否为验证数据"
    )

    is_test_data = models.BooleanField(
        default=False,
        verbose_name="是否为测试数据",
        help_text="是否为测试数据"
    )

    # 日志聚类特有字段
    log_count = models.IntegerField(
        default=0,
        verbose_name="日志条数",
        help_text="数据集中包含的日志条数"
    )

    log_source = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="日志来源",
        help_text="日志数据的来源系统或文件"
    )

    class Meta:
        verbose_name = "日志聚类训练数据"
        verbose_name_plural = "日志聚类训练数据"

    def __str__(self):
        return f"{self.name} - {self.dataset.name}"