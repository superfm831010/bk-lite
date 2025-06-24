from typing import Optional
from pydantic import BaseModel, Field


class AnomalyDetectionTrainResponse(BaseModel):
    """异常检测训练响应"""

    task_id: str = Field(..., description="任务ID，用于查询训练状态")
    experiment_name: str = Field(..., description="实验名称")
    status: str = Field(..., description="训练状态：started")
    message: Optional[str] = Field(default="训练任务已启动", description="状态消息")
