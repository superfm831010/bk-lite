# -- coding: utf-8 --
# @File: alert_rules.py
# @Time: 2025/5/21 10:58
# @Author: windyzhao
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, validator
from enum import Enum


class SeverityLevel(str, Enum):
    WARNING = "warning"
    SEVERITY = "severity"
    FATAL = "fatal"


class ConditionType(str, Enum):
    THRESHOLD = "threshold"  # 阈值告警
    SUSTAINED = "sustained"  # 持续告警
    TREND = "trend"  # 趋势告警
    PREV_FIELD = "prev_field_equals"  # 前置状态告警


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
    min_data_points: int = 2

    @validator('operator')
    def validate_operator(cls, v):
        if v and v not in ['>', '>=', '<', '<=', '==', '!=']:  # 添加 != 支持
            raise ValueError(f"Invalid operator: {v}")
        return v


class AlertRuleConfig(BaseModel):
    name: str
    description: str
    severity: SeverityLevel = SeverityLevel.WARNING
    is_active: bool = True
    title: str = None  # 自定义告警标题，支持变量替换
    content: str = None  # 自定义告警内容，支持变量替换
    condition: ConditionConfig


class AlertRulesConfig(BaseModel):
    window_size: str = "10min"
    rules: List[AlertRuleConfig]


DEFAULT_TITLE = "【${resource_type}】${resource_name}发生${item} 异常"
DEFAULT_CONTENT = "【${resource_type}】${resource_name}发生${item} 异常"


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


RULES = {
    "window_size": "10min",
    "rules": [
        {
            "name": "high_cpu",
            "description": "CPU使用率超过85%",
            "severity": "warning",
            "condition": {
                "type": "threshold",
                "field": "cpu_usage",
                "threshold": 85,
                "operator": ">="
            }
        },
        {
            "name": "sustained_high_cpu",
            "description": "CPU连续3个周期使用率超过80%",
            "severity": "warning",
            "condition": {
                "type": "sustained",
                "field": "cpu_usage",
                "threshold": 80,
                "operator": ">=",
                "required_consecutive": 3
            }
        },
        {
            "name": "disk_io_latency_spike",
            "description": "磁盘IO延迟大于5.0",
            "severity": "severity",
            "condition": {
                "type": "threshold",
                "field": "disk_io_latency",
                "threshold": 5.0,
                "operator": ">"
            }
        },
        {
            "name": "cpu_trend_spike",
            "description": "CPU使用率突增超过20%",
            "severity": "fatal",
            "condition": {
                "type": "trend",
                "field": "cpu_usage",
                "threshold": 20,
                "operator": ">",
                "baseline_window": 5,
                "trend_method": "percentage"
            }
        },
        {
            "name": "prev_status_equals",
            "description": "当同一source、obj、obj_inst, metric的上一条event状态为close且本次满足条件时，创建alert并关联",
            "severity": "fatal",
            "condition": {
                "field": "",
                "type": "prev_field_equals",
                "group_by": ["source_id", "resource_type", "resource_id", "item"],
                "prev_status_field": "status",
                "prev_status_value": "closed"
            }
        },
        {
            "name": "jenkins_single_failure",
            "description": "Jenkins单次构建失败",
            "severity": "warning",
            "title": "Jenkins构建失败 - ${resource_name}",
            "content": "流水线: ${resource_name}\n状态: 构建失败\n构建号: ${value}\n错误信息: ${description}",
            "condition": {
                "type": "threshold",
                "field": "status",
                "threshold": 0,
                "operator": "=="
            }
        },
        {
            "name": "jenkins_sustained_failures",
            "description": "Jenkins构建连续失败3次",
            "severity": "fatal",
            "title": "Jenkins流水线 ${resource_name} 连续构建失败",
            "content": "流水线: ${resource_name}\n连续失败次数: 3次",
            "condition": {
                "type": "sustained",
                "field": "build_status",
                "threshold": 0,
                "operator": "==",
                "required_consecutive": 3,
                "group_by": ["resource_id"]
            }
        },
    ]
}


def load_rules(config: Dict[str, Any]) -> AlertRulesConfig:
    """加载并验证规则配置"""
    return AlertRulesConfig(**config)


# 验证规则
VALID_RULES = load_rules(RULES)
