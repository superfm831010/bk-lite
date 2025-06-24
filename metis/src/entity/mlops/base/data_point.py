from typing import List, Optional
from pydantic import BaseModel, Field


class DataPoint(BaseModel):
    """时间序列数据点结构"""
    timestamp: str = Field(..., description="时间戳，ISO 8601格式")
    value: float = Field(..., description="数值")
