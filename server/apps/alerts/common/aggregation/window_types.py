# -- coding: utf-8 --
# @File: window_types.py
# @Time: 2025/6/30 14:00
# @Author: windyzhao

from enum import Enum
from dataclasses import dataclass
from datetime import timedelta


class WindowType(str, Enum):
    """聚合窗口类型"""
    SLIDING = "sliding"  # 滑动窗口 - 当前实现
    FIXED = "fixed"  # 固定窗口
    SESSION = "session"  # 会话窗口


@dataclass
class WindowConfig:
    """窗口配置"""
    window_type: str
    window_size: str = "10min"

    # 滑动窗口特有配置
    slide_interval: str = "1min"  # 滑动间隔

    # 固定窗口特有配置
    alignment: str = "minute"  # 对齐方式: minute, hour, day

    # 会话窗口特有配置
    session_timeout: str = "5min"  # 会话超时时间
    session_key_fields: list = None  # 会话分组字段，空数组表示使用事件指纹

    # 通用配置
    max_window_size: str = "1h"  # 最大窗口大小限制

    def __post_init__(self):
        if self.session_key_fields is None:
            # 默认使用指纹分组模式（空数组）
            self.session_key_fields = []

    @property
    def use_fingerprint_grouping(self) -> bool:
        """
        是否使用指纹分组模式
        
        指纹分组模式的优势：
        1. 每个唯一事件组合（资源+指标+告警源等）独立成会话
        2. 简化会话管理逻辑，提高性能
        3. 更精细的粒度控制，避免不相关事件混合
        
        Returns:
            bool: True表示使用指纹分组，False表示使用字段组合分组
        """
        return True


class WindowCalculator:
    """窗口时间计算器"""

    @staticmethod
    def parse_time_str(time_str: str) -> timedelta:
        """解析时间字符串为timedelta对象"""
        if time_str.endswith('min'):
            return timedelta(minutes=int(time_str[:-3]))
        elif time_str.endswith('h'):
            return timedelta(hours=int(time_str[:-1]))
        elif time_str.endswith('d'):
            return timedelta(days=int(time_str[:-1]))
        elif time_str.endswith('s'):
            return timedelta(seconds=int(time_str[:-1]))
        else:
            # 默认按分钟处理
            return timedelta(minutes=int(time_str))
