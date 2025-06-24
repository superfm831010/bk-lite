from typing import List
from pydantic import BaseModel, Field
from src.entity.mlops.anomaly_detection.anomaly_prediction_result import AnomalyPredictionResult


class AnomalyDetectionPredictResponse(BaseModel):
    """异常检测预测响应"""

    model_name: str = Field(..., description="使用的模型名称")
    model_version: str = Field(..., description="使用的模型版本")

    # 预测结果（对象数组格式）
    predictions: List[AnomalyPredictionResult] = Field(
        ..., description="预测结果列表")

    # 统计信息
    total_points: int = Field(..., description="总数据点数")
    anomaly_count: int = Field(..., description="异常点数量")
    anomaly_rate: float = Field(..., description="异常率")
