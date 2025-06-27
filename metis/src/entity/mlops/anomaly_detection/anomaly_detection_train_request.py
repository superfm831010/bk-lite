from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from src.entity.mlops.base.training_data_point import TrainingDataPoint


class AnomalyDetectionTrainRequest(BaseModel):
    """异常检测训练请求"""

    algorithm: str = Field(
        default="RandomForest", description="异常检测算法名称，默认为RandomForest")

    experiment_name: str = Field(..., description="实验名称，用于MLflow实验管理")

    # 数据集（对象数组格式）
    train_data: List[TrainingDataPoint] = Field(..., description="训练数据")
    val_data: List[TrainingDataPoint] = Field(..., description="验证数据")
    test_data: List[TrainingDataPoint] = Field(..., description="测试数据")

    # 数据处理参数
    freq: str = Field(
        default="infer", description="时间序列频率，如'1H', '1D'等，默认自动推断")
    window: int = Field(default=30, description="滚动窗口大小，用于特征工程")
    random_state: int = Field(default=42, description="随机种子")

    # 超参数优化配置
    hyperopt_config: Optional[Dict[str, Any]] = Field(
        default=None,
        description="超参数优化配置，包含space、max_evals等参数"
    )
