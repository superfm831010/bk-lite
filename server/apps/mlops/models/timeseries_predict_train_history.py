from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.mlops.models.data_points_features_info import DataPointFeaturesInfo


class TimeSeriesPredictTrainHistory(MaintainerInfo, TimeInfo, DataPointFeaturesInfo):
    algorithm = models.CharField(
        max_length=50,
        verbose_name="算法模型",
        help_text="使用的时间序列预测算法模型",
        choices=[
            ('Prophet', 'Prophet'),
        ]
    )

    train_data_id = models.ForeignKey(
        'TimeSeriesPredictTrainData',
        on_delete=models.CASCADE,
        related_name="train_history",
        verbose_name="训练数据集",
        help_text="关联的时间序列预测训练数据集"
    )
    val_data_id = models.ForeignKey(
        'TimeSeriesPredictTrainData',
        on_delete=models.CASCADE,
        related_name="val_history",
        verbose_name="验证数据集",
        help_text="关联的时间序列预测验证数据集"
    )

    test_data_id = models.ForeignKey(
        'TimeSeriesPredictTrainData',
        on_delete=models.CASCADE,
        related_name="test_history",
        verbose_name="测试数据集",
        help_text="关联的时间序列预测测试数据集"
    )
    
    hyperopt_config = models.JSONField(
        verbose_name="超参数优化配置",
        help_text="用于超参数优化的配置参数",
        default=dict,
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('running', '训练中'),
            ('completed', '已完成'),
            ('failed', '训练失败'),
        ],
        default='pending',
        verbose_name="任务状态",
        help_text="训练任务的当前状态"
    )

    class Meta:
        verbose_name = "时间序列预测训练历史"
        verbose_name_plural = "时间序列预测训练历史"
