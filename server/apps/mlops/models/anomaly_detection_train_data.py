from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.anomaly_detection_dataset import AnomalyDetectionDataset
from django_minio_backend import MinioBackend, iso_date_prefix


class AnomalyDetectionTrainData(MaintainerInfo, TimeInfo):
    """异常检测训练数据模型"""

    name = models.CharField(max_length=100, verbose_name="训练数据名称")
    
    dataset = models.ForeignKey(
        AnomalyDetectionDataset,
        on_delete=models.CASCADE,
        related_name="train_data",
        verbose_name="数据集",
    )
    
    train_data = models.JSONField(
        verbose_name="训练数据",
        help_text="存储训练数据",
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
    
    anomaly_point_count = models.PositiveIntegerField(
        default=0,
        verbose_name="异常点数量",
        help_text="异常点的数量"
    )

    class Meta:
        verbose_name = "异常检测训练数据"
        verbose_name_plural = "异常检测训练数据"

    def __str__(self):
        return f"{self.name} - {self.dataset.name}"

    def save(self, *args, **kwargs):
        """
        保存时自动计算异常点数量
        从metadata中的anomaly_point数组长度获取异常点数量
        """
        if self.metadata:
            anomaly_point = self.metadata.get('anomaly_point', [])
            self.anomaly_point_count = len(anomaly_point)
        else:
            self.anomaly_point_count = 0
        
        super().save(*args, **kwargs)
