from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, root_validator


class AnomalyDetectionTrainRequest(BaseModel):
    """异常检测算法训练请求"""
    algorithm: str = Field('', description="算法名称，支持xgbod/randomforest/iforest")
    train_config: Dict[str, Any] = Field({}, description="训练配置参数")
    supervised: bool = Field(False, description="是否有监督学习")
    job_id: str = Field('', description="训练任务ID")
    run_mode: str = Field('local', description="运行模式，local为本地，remote为远程")

    # 兼容旧版请求
    run_model: Optional[str] = Field(None, description="已弃用，请使用run_mode")

    @root_validator(pre=True)
    def check_params(cls, values):
        # 处理run_model -> run_mode的问题
        if 'run_model' in values and 'run_mode' not in values:
            values['run_mode'] = values.pop('run_model')
        return values

    class Config:
        extra = "allow"  # 允许额外字段
