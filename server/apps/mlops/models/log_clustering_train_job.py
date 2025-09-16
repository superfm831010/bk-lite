from django.db import models
from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class LogClusteringTrainJob(MaintainerInfo, TimeInfo):
    """日志聚类训练任务"""

    name = models.CharField(max_length=100, verbose_name="任务名称")
    description = models.TextField(blank=True, null=True, verbose_name="任务描述")

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待训练'),
            ('running', '训练中'),
            ('completed', '已完成'),
            ('failed', '训练失败'),
        ],
        default='pending',
        verbose_name="任务状态",
        help_text="训练任务的当前状态"
    )

    algorithm = models.CharField(
        max_length=50,
        verbose_name="算法模型",
        help_text="使用的日志聚类算法模型",
        choices=[
            ('KMeans', 'K-Means'),
            ('DBSCAN', 'DBSCAN'),
            ('AgglomerativeClustering', '层次聚类'),
            ('Drain', 'Drain'),
            ('LogCluster', 'LogCluster'),
        ]
    )

    train_data_id = models.ForeignKey(
        'LogClusteringTrainData',
        on_delete=models.CASCADE,
        related_name="train_jobs",
        verbose_name="训练数据集",
        help_text="关联的日志聚类训练数据集"
    )

    val_data_id = models.ForeignKey(
        'LogClusteringTrainData',
        on_delete=models.CASCADE,
        related_name="val_jobs",
        verbose_name="验证数据集",
        help_text="关联的日志聚类验证数据集",
        blank=True,
        null=True
    )

    test_data_id = models.ForeignKey(
        'LogClusteringTrainData',
        on_delete=models.CASCADE,
        related_name="test_jobs",
        verbose_name="测试数据集",
        help_text="关联的日志聚类测试数据集",
        blank=True,
        null=True
    )

    hyperopt_config = models.JSONField(
        verbose_name="超参数优化配置",
        help_text="用于超参数优化的配置参数",
        default=dict,
    )

    max_evals = models.IntegerField(
        default=200,
        verbose_name="最大评估次数",
        help_text="超参数优化的最大评估次数"
    )

    # 日志聚类特有参数
    cluster_count = models.IntegerField(
        default=10,
        verbose_name="聚类数量",
        help_text="预期的聚类簇数量（适用于K-Means等算法）"
    )

    min_samples = models.IntegerField(
        default=5,
        verbose_name="最小样本数",
        help_text="形成聚类所需的最小样本数（适用于DBSCAN等算法）"
    )

    eps = models.FloatField(
        default=0.5,
        verbose_name="邻域半径",
        help_text="DBSCAN算法的邻域半径参数"
    )
    
    class Meta:
        verbose_name = "日志聚类训练任务"
        verbose_name_plural = "日志聚类训练任务"

    def __str__(self):
        return self.name