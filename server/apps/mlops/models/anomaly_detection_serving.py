from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from django.db import models

from apps.mlops.models.anomaly_detection_train_job import AnomalyDetectionTrainJob


class AnomalyDetectionServing(MaintainerInfo, TimeInfo):
    name = models.CharField(
        max_length=100,
        verbose_name="服务名称",
        help_text="服务的名称",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="服务描述",
        help_text="服务的详细描述",
    )
    anomaly_detection_train_job = models.ForeignKey(
        AnomalyDetectionTrainJob,
        on_delete=models.CASCADE,
        related_name="servings",
        verbose_name="模型ID",
        help_text="关联的异常检测训练任务模型ID",
    )
    model_version = models.CharField(
        max_length=50,
        default="latest",
        verbose_name="模型版本",
        help_text="模型版本",
    )
    status= models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive")
        ],
        default="active",
        verbose_name="服务状态",
        help_text="服务的当前状态",
    )
    anomaly_threshold = models.FloatField(
        default=0.5,
        verbose_name="异常阈值",
        help_text="用于判断异常的阈值",
    )
    
    class Meta:
        verbose_name = "异常检测服务"
        verbose_name_plural = "异常检测服务"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.name}"
