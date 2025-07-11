# -- coding: utf-8 --
# @File: alert_rules.py
# @Time: 2025/5/21 10:58
# @Author: windyzhao
from typing import List, Dict, Any, Tuple, Union
from pydantic import BaseModel, validator, ValidationError
from enum import Enum
from apps.core.logger import alert_logger as logger

DEFAULT_TITLE = "【${resource_type}】${resource_name}发生${item} 异常"
DEFAULT_CONTENT = "【${resource_type}】${resource_name}发生${item} 异常"


class SeverityLevel(str, Enum):
    WARNING = "warning"
    SEVERITY = "severity"
    FATAL = "fatal"


class ConditionType(str, Enum):
    THRESHOLD = "threshold"  # 阈值告警
    SUSTAINED = "sustained"  # 持续告警
    TREND = "trend"  # 趋势告警
    PREV_FIELD_EQUALS = "prev_field_equals"  # 前置状态告警
    LEVEL_FILTER = "level_filter"
    WEBSITE_MONITORING = "website_monitoring"
    FILTER_AND_CHECK = "filter_and_check"  # 通用过滤检查


class ConditionConfig(BaseModel):
    type: ConditionType
    field: str
    threshold: float = None
    operator: str = None
    required_consecutive: int = None
    baseline_window: int = None
    trend_method: str = "absolute"
    group_by: List[str] = None
    prev_status_field: str = None
    prev_status_value: str = None
    # 添加缺失的字段
    level_threshold: str = None
    aggregation_key: List[str] = None
    status_field: str = None
    abnormal_status: str = None
    immediate_alert: bool = False

    # 新增通用过滤检查字段 - 支持任意类型
    filter: Dict[str, Any] = None  # 过滤条件字典
    target_field: str = None  # 目标检查字段
    target_field_value: Union[str, int, float, bool, None] = None  # 目标字段的期望值
    target_value_field: str = None  # 目标值字段
    target_value: Union[str, int, float, bool, None] = None  # 目标值，用于特定条件类型的期望值比较
    session_close: dict = {}

    @validator('operator')
    def validate_operator(cls, v):
        if v and v not in ['>', '>=', '<', '<=', '==', '!=', 'in', 'not_in']:  # 添加 in 和 not_in 支持
            raise ValueError(f"Invalid operator: {v}")
        return v

    @validator('target_field')
    def validate_target_field(cls, v):
        return v


class AlertRuleConfig(BaseModel):
    name: str
    rule_id: str
    description: dict
    severity: SeverityLevel = SeverityLevel.WARNING
    is_active: bool = True
    title: str = None  # 自定义告警标题，支持变量替换
    content: str = None  # 自定义告警内容，支持变量替换
    condition: ConditionConfig


class AlertRulesConfig(BaseModel):
    window_size: str = "10min"
    window_type: str = "sliding"  # 新增：窗口类型
    alignment: str = "natural"  # 新增：对齐方式
    max_window_size: str = "1h"  # 新增：最大窗口大小
    session_timeout: str = "30m"  # 新增：会话超时时间
    session_key_fields: List[str] = ['item', 'resource_id', 'resource_type', 'alert_source',
                                     'rule_id']  # 会话键字段和event指纹一致
    rules: List[AlertRuleConfig]


def format_template_string(template: str, data: Dict[str, Any]) -> str:
    """格式化模板字符串中的变量

    Args:
        template: 包含${变量名}格式的模板字符串
        data: 包含变量名和对应值的字典

    Returns:
        格式化后的字符串
    """
    if not template:
        return ""

    result = template
    # 替换所有${var}格式的变量
    for key, value in data.items():
        placeholder = "${" + key + "}"
        if not value:
            value = ""
        result = result.replace(placeholder, str(value))

    return result


def format_alert_message(rule: AlertRuleConfig, event_data: Dict[str, Any]) -> Tuple[str, str]:
    """格式化告警标题和内容

    Args:
        rule: 告警规则配置
        event_data: 触发事件的数据

    Returns:
        包含格式化后标题和内容的字典
    """
    title = getattr(rule, "title", None)
    content = getattr(rule, "content", None)

    # 如果规则中没有设置标题或内容，使用默认格式
    if not title:
        title = DEFAULT_TITLE
    if not content:
        content = DEFAULT_CONTENT

    # 格式化标题和内容
    formatted_title = format_template_string(title, event_data)
    formatted_content = format_template_string(content, event_data)

    return formatted_title, formatted_content


def load_rules(config: Dict[str, Any]) -> AlertRulesConfig:
    """加载并验证规则配置"""
    try:
        logger.info("开始加载告警规则配置")
        config = AlertRulesConfig(**config)
        logger.info(f"成功加载 {len(config.rules)} 条告警规则")
        return config
    except ValidationError as e:
        logger.error(f"告警规则配置验证失败: {e}")
        # 记录详细的验证错误信息
        for error in e.errors():
            logger.error(f"验证错误 - 字段: {error['loc']}, 错误类型: {error['type']}, 输入值: {error['input']}")
        raise
    except Exception as e:
        logger.error(f"加载告警规则配置时发生未知错误: {e}")
        raise
