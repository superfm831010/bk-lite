from typing import List, Optional

from pydantic import BaseModel, Field, root_validator


class DataPoint(BaseModel):
    """
    时间序列数据点结构

    属性:
        timestamp: 时间戳，ISO 8601格式字符串
        value: 数据点数值
    """
    timestamp: str = Field(..., description="时间戳，ISO 8601格式")
    value: float = Field(..., description="数据点数值")


class AnomalyDetectionPredictRequest(BaseModel):
    pass
