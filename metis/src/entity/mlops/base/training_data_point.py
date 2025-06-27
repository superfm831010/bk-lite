from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class TrainingDataPoint(BaseModel):
    """训练数据点结构"""
    timestamp: str = Field(..., description="时间戳，ISO 8601格式")
    value: float = Field(..., description="数值")
    label: int = Field(..., description="标签，0=正常，1=异常")
