# -- coding: utf-8 --
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum


class SeverityLevel(str, Enum):
    WARNING = "warning"
    SEVERITY = "severity"
    FATAL = "fatal"


class ConditionType(str, Enum):
    THRESHOLD = "threshold"
    SUSTAINED = "sustained"
    TREND = "trend"
    PREV_FIELD = "prev_field_equals"
    LEVEL_FILTER = "level_filter"
    WEBSITE_MONITORING = "website_monitoring"
    FILTER_AND_CHECK = "filter_and_check"  # 新增通用过滤检查类型


@dataclass
class RuleCondition:
    """规则条件配置"""
    type: ConditionType  # 条件类型，如阈值、持续性、趋势等
    field: str  # 监控字段名，用于从事件数据中提取值进行判断
    threshold: float = None  # 阈值，用于阈值类型条件的数值比较
    operator: str = None  # 比较操作符，如 '>', '<', '>=', '<=', '=', '!='
    required_consecutive: int = None  # 持续性条件所需的连续触发次数
    baseline_window: int = None  # 基线窗口大小（分钟），用于趋势分析的历史数据范围
    trend_method: str = "absolute"  # 趋势计算方法：absolute(绝对值) 或 percentage(百分比)
    group_by: List[str] = None  # 分组字段列表，用于按指定字段对事件进行分组处理
    prev_status_field: str = None  # 前置状态字段名，用于状态变化检测
    prev_status_value: str = None  # 前置状态期望值，与当前状态比较判断是否发生变化
    min_data_points: int = 2  # 最小数据点数量，趋势分析所需的最少历史数据点
    # 扩展字段
    level_threshold: str = None  # 级别阈值，用于级别过滤条件的严重程度判断
    aggregation_key: List[str] = None  # 聚合键列表，用于事件聚合时的分组依据
    status_field: str = None  # 状态字段名，用于监控状态变化的字段
    abnormal_status: str = None  # 异常状态值，定义触发告警的异常状态
    immediate_alert: bool = False  # 是否立即告警，跳过持续性检查直接触发

    # 新增通用过滤检查字段 - 支持任意类型
    filter: Dict[str, Any] = None  # 过滤条件字典
    target_field: str = None  # 目标检查字段
    target_field_value: Union[str, int, float, bool, None] = None  # 目标字段的期望值
    target_value_field: str = None  # 目标值字段
    target_value: Union[str, int, float, bool, None] = None  # 目标值，用于特定条件类型的期望值比较

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "type": self.type.value,
            "field": self.field,
            "threshold": self.threshold,
            "operator": self.operator,
            "required_consecutive": self.required_consecutive,
            "baseline_window": self.baseline_window,
            "trend_method": self.trend_method,
            "group_by": self.group_by,
            "prev_status_field": self.prev_status_field,
            "prev_status_value": self.prev_status_value,
            "min_data_points": self.min_data_points,
            "filter": self.filter,
            "target_field": self.target_field,
            "target_field_value": self.target_field_value,
            "target_value_field": self.target_value_field,
            "target_value": self.target_value,
        }


@dataclass
class AlertRule:
    """告警规则基类"""
    name: str
    description: str
    severity: SeverityLevel = SeverityLevel.WARNING
    is_active: bool = True
    title: str = None
    content: str = None
    condition: RuleCondition = None

    def get_formatted_title(self, event_data: Dict[str, Any]) -> str:
        """获取格式化后的标题"""
        from apps.alerts.common.rules.alert_rules import format_template_string, DEFAULT_TITLE
        title = self.title or DEFAULT_TITLE
        return format_template_string(title, event_data)

    def get_formatted_content(self, event_data: Dict[str, Any]) -> str:
        """获取格式化后的内容"""
        from apps.alerts.common.rules.alert_rules import format_template_string, DEFAULT_CONTENT
        content = self.content or DEFAULT_CONTENT
        return format_template_string(content, event_data)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "description": self.description,
            "severity": self.severity.value,
            "is_active": self.is_active,
            "title": self.title,
            "content": self.content,
            "condition": self.condition.to_dict() if self.condition else None
        }
