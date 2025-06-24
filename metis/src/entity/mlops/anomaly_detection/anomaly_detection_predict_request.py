from typing import List, Optional
from pydantic import BaseModel, Field
from src.entity.mlops.base.data_point import DataPoint


class AnomalyDetectionPredictRequest(BaseModel):
    algorithm: str = Field(..., description="异常检测算法名称")
    model_name: str = Field(..., description="模型名称")
    model_version: Optional[str] = Field(
        default="latest", description="模型版本，默认为latest")
    data: List[DataPoint] = Field(..., description="时间序列数据点列表")
    anomaly_threshold: Optional[float] = Field(
        default=0.5, description="异常检测阈值，默认为0.5")
