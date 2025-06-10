# -- coding: utf-8 --
from abc import ABC, abstractmethod
from typing import List, Dict, Any
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


@dataclass
class RuleCondition:
    """规则条件配置"""
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
            "condition": {
                "type": self.condition.type.value,
                "field": self.condition.field,
                "threshold": self.condition.threshold,
                "operator": self.condition.operator,
                "required_consecutive": self.condition.required_consecutive,
                "baseline_window": self.condition.baseline_window,
                "trend_method": self.condition.trend_method,
                "group_by": self.condition.group_by,
                "prev_status_field": self.condition.prev_status_field,
                "prev_status_value": self.condition.prev_status_value,
                "min_data_points": self.condition.min_data_points,
            } if self.condition else None
        }


class BaseRuleSet(ABC):
    """规则集基类"""
    
    @abstractmethod
    def get_rules(self) -> List[AlertRule]:
        """获取规则列表"""
        pass
    
    @property
    @abstractmethod
    def window_size(self) -> str:
        """时间窗口大小"""
        pass
