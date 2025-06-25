from typing import List
from pydantic import BaseModel, Field


class AnomalyPredictionResult(BaseModel):
    """单个异常检测结果"""
    timestamp: str = Field(..., description="时间戳")
    value: float = Field(..., description="原始数值")
    anomaly_probability: float = Field(..., description="异常概率 (0-1)")
    is_anomaly: bool = Field(..., description="是否为异常点")
