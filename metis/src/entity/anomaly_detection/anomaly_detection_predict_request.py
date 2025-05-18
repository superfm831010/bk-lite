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
    """
    异常检测预测请求

    属性:
        model_id: 模型ID
        algorithm: 算法名称，支持xgbod/randomforest/iforest
        run_mode: 运行模式，local为本地，remote为远程
        run_model: 已弃用，请使用run_mode
        predict_data: 预测数据点列表
    """
    model_id: str = Field(..., description="模型ID")
    algorithm: str = Field('', description="算法名称，支持xgbod/randomforest/iforest")
    run_mode: str = Field('local', description="运行模式，local为本地，remote为远程")
    run_model: Optional[str] = Field(None, description="已弃用，请使用run_mode")
    predict_data: List[DataPoint] = Field(..., description="预测数据点列表")

    @root_validator(pre=True)
    def check_params(cls, values):
        """处理参数兼容性问题"""
        # 处理run_model -> run_mode的问题
        if 'run_model' in values and 'run_mode' not in values:
            values['run_mode'] = values.pop('run_model')
        return values

    class Config:
        extra = "allow"  # 允许额外字段
