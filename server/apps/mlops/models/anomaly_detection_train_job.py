from random import choice
from django.db import models
from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.data_points_features_info import DataPointFeaturesInfo


class AnomalyDetectionTrainJob(MaintainerInfo, TimeInfo, DataPointFeaturesInfo):
    """异常检测训练任务"""

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
        help_text="使用的异常检测算法模型",
        choices=[
            ('RandomForest', '随机森林'),
        ]
    )

    train_data_id = models.ForeignKey(
        'AnomalyDetectionTrainData',
        on_delete=models.CASCADE,
        related_name="train_jobs",
        verbose_name="训练数据集",
        help_text="关联的异常检测训练数据集"
    )

    val_data_id = models.ForeignKey(
        'AnomalyDetectionTrainData',
        on_delete=models.CASCADE,
        related_name="val_jobs",
        verbose_name="验证数据集",
        help_text="关联的异常检测验证数据集"
    )

    test_data_id = models.ForeignKey(
        'AnomalyDetectionTrainData',
        on_delete=models.CASCADE,
        related_name="test_jobs",
        verbose_name="测试数据集",
        help_text="关联的异常检测测试数据集"
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
    
    class Meta:
        verbose_name = "异常检测训练任务"
        verbose_name_plural = "异常检测训练任务"
