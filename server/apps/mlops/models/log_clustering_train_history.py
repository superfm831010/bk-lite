from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.data_points_features_info import DataPointFeaturesInfo


class LogClusteringTrainHistory(MaintainerInfo, TimeInfo, DataPointFeaturesInfo):
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
        related_name="train_history",
        verbose_name="训练数据集",
        help_text="关联的日志聚类训练数据集"
    )
    
    val_data_id = models.ForeignKey(
        'LogClusteringTrainData',
        on_delete=models.CASCADE,
        related_name="val_history",
        verbose_name="验证数据集",
        help_text="关联的日志聚类验证数据集",
        blank=True,
        null=True
    )

    test_data_id = models.ForeignKey(
        'LogClusteringTrainData',
        on_delete=models.CASCADE,
        related_name="test_history",
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

    # 日志聚类特有训练结果字段
    cluster_count = models.IntegerField(
        default=0,
        verbose_name="实际聚类数量",
        help_text="训练后实际产生的聚类簇数量"
    )

    silhouette_score = models.FloatField(
        blank=True,
        null=True,
        verbose_name="轮廓系数",
        help_text="聚类质量评估的轮廓系数"
    )

    davies_bouldin_score = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Davies-Bouldin指数",
        help_text="聚类质量评估的Davies-Bouldin指数"
    )

    calinski_harabasz_score = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Calinski-Harabasz指数",
        help_text="聚类质量评估的Calinski-Harabasz指数"
    )

    class Meta:
        verbose_name = "日志聚类训练历史"
        verbose_name_plural = "日志聚类训练历史"

    def __str__(self):
        return f"{self.algorithm} - {self.status}"