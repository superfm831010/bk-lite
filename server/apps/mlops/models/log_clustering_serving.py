from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from django.db import models

from apps.mlops.models.log_clustering_train_job import LogClusteringTrainJob


class LogClusteringServing(MaintainerInfo, TimeInfo):
    name = models.CharField(
        max_length=100,
        verbose_name="服务名称",
        help_text="日志聚类服务的名称",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="服务描述",
        help_text="日志聚类服务的详细描述",
    )
    log_clustering_train_job = models.ForeignKey(
        LogClusteringTrainJob,
        on_delete=models.CASCADE,
        related_name="servings",
        verbose_name="模型ID",
        help_text="关联的日志聚类训练任务模型ID",
    )
    model_version = models.CharField(
        max_length=50,
        default="latest",
        verbose_name="模型版本",
        help_text="模型版本",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive")
        ],
        default="active",
        verbose_name="服务状态",
        help_text="服务的当前状态",
    )

    # 日志聚类服务特有字段
    api_endpoint = models.URLField(
        blank=True,
        null=True,
        verbose_name="API端点",
        help_text="日志聚类服务的API访问端点"
    )

    max_requests_per_minute = models.IntegerField(
        default=1000,
        verbose_name="每分钟最大请求数",
        help_text="服务的请求频率限制"
    )

    supported_log_formats = models.JSONField(
        default=list,
        verbose_name="支持的日志格式",
        help_text="服务支持的日志格式列表"
    )
 
    
    class Meta:
        verbose_name = "日志聚类服务"
        verbose_name_plural = "日志聚类服务"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.name}"