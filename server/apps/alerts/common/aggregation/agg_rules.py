# -- coding: utf-8 --
# @File: agg_rules.py
# @Time: 2025/6/16 15:23
# @Author: windyzhao

"""
聚合规则配置模块
定义不同窗口类型的聚合规则配置
"""

from typing import Dict, List, Any
from enum import Enum


class WindowType(str, Enum):
    """窗口类型枚举"""
    SLIDING = "sliding"  # 滑动窗口
    FIXED = "fixed"  # 固定窗口
    SESSION = "session"  # 会话窗口


class AggregationStrategy(str, Enum):
    """聚合策略枚举"""
    GROUP_BY = "group_by"  # 按字段分组
    MERGE_ALL = "merge_all"  # 合并所有
    CREATE_NEW = "create_new"  # 总是创建新告警


# 窗口类型处理优先级
WINDOW_TYPE_PRIORITY = [
    WindowType.SLIDING,
    WindowType.FIXED,
    WindowType.SESSION
]

# 各窗口类型的默认配置
DEFAULT_WINDOW_CONFIGS = {
    WindowType.SLIDING: {
        'window_size': '10min',
        'slide_interval': '1min',
        'alignment': 'natural',
        'max_window_size': '1h',
        'execution_frequency': 'every_minute'  # 每分钟执行
    },
    WindowType.FIXED: {
        'window_size': '5min',
        'slide_interval': '5min',
        'alignment': 'minute',  # 改为支持的对齐方式
        'max_window_size': '1h',
        'execution_frequency': 'window_aligned'  # 按窗口对齐执行
    },
    WindowType.SESSION: {
        'window_size': '15min',
        'session_timeout': '30min',
        'session_key_fields': ['item', 'resource_id', 'resource_type', 'alert_source', 'rule_id'], # 会话键字段和event指纹一致,
        'max_window_size': '2h',
        'max_event_count': 1000,  # 最大事件数量
        'execution_frequency': 'timeout_based'  # 基于超时时间执行
    }
}


def get_window_config(window_type: WindowType) -> Dict[str, Any]:
    """获取窗口类型的默认配置"""
    return DEFAULT_WINDOW_CONFIGS.get(window_type, {})


def validate_window_config(config: Dict[str, Any]) -> bool:
    """验证窗口配置的有效性"""
    required_fields = ['window_size', 'window_type']
    return all(field in config for field in required_fields)
