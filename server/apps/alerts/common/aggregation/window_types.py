# -- coding: utf-8 --
# @File: window_types.py
# @Time: 2025/6/30 14:00
# @Author: windyzhao

from enum import Enum
from typing import Dict
from dataclasses import dataclass
from datetime import datetime, timedelta


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

    @staticmethod
    def get_sliding_window_range(current_time: datetime, config: WindowConfig) -> tuple:
        """获取滑动窗口的时间范围"""
        window_delta = WindowCalculator.parse_time_str(config.window_size)
        start_time = current_time - window_delta
        end_time = current_time
        return start_time, end_time

    @staticmethod
    def get_fixed_window_range(current_time: datetime, config: WindowConfig) -> tuple:
        """获取固定窗口的时间范围 - 修正版本"""
        window_delta = WindowCalculator.parse_time_str(config.window_size)

        # 根据对齐方式计算窗口边界
        if config.alignment == "minute":
            # 对齐到分钟
            aligned_time = current_time.replace(second=0, microsecond=0)
            # 计算窗口大小（分钟）
            window_minutes = int(window_delta.total_seconds() / 60)
            # 找到当前时间所属的窗口开始时间
            current_minute = aligned_time.minute
            window_start_minute = (current_minute // window_minutes) * window_minutes
            start_time = aligned_time.replace(minute=window_start_minute)

        elif config.alignment == "hour":
            # 对齐到小时
            aligned_time = current_time.replace(minute=0, second=0, microsecond=0)
            # 计算窗口大小（小时）
            window_hours = int(window_delta.total_seconds() / 3600)
            # 找到当前时间所属的窗口开始时间
            current_hour = aligned_time.hour
            window_start_hour = (current_hour // window_hours) * window_hours
            start_time = aligned_time.replace(hour=window_start_hour)

        elif config.alignment == "day":
            # 对齐到天
            aligned_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
            # 计算窗口大小（天）
            window_days = int(window_delta.total_seconds() / 86400)
            # 找到当前时间所属的窗口开始时间
            days_since_epoch = (aligned_time.date() - datetime.date(1970, 1, 1)).days
            window_start_days = (days_since_epoch // window_days) * window_days
            start_time = datetime.datetime.combine(
                datetime.date(1970, 1, 1) + timedelta(days=window_start_days),
                datetime.time(0, 0, 0)
            )
            start_time = start_time.replace(tzinfo=aligned_time.tzinfo)
        else:
            # 默认按分钟对齐
            aligned_time = current_time.replace(second=0, microsecond=0)
            start_time = aligned_time - window_delta

        end_time = start_time + window_delta
        return start_time, end_time

    @staticmethod
    def get_session_window_ranges(events_df, config: WindowConfig) -> Dict[str, tuple]:
        """获取会话窗口的时间范围
        
        会话窗口特点：
        - 基于事件活动动态调整窗口大小
        - 当事件间隔超过超时时间时结束会话
        - 适用于用户行为分析、故障关联分析
        
        Args:
            events_df: 事件数据DataFrame
            config: 窗口配置
            
        Returns:
            Dict[str, tuple]: 会话键到时间范围的映射
        """
        if events_df.empty:
            return {}

        session_timeout = WindowCalculator.parse_time_str(config.session_timeout)
        session_ranges = {}

        # 按会话分组字段分组
        try:
            # 修复：确保分组字段存在于数据中
            available_fields = [field for field in config.session_key_fields if field in events_df.columns]
            if not available_fields:
                # 如果没有可用的分组字段，使用默认分组
                available_fields = ['event_id']  # 每个事件独立成会话

            grouped = events_df.groupby(available_fields)

            for group_key, group_df in grouped:
                # 按时间排序
                sorted_df = group_df.sort_values('received_at')

                session_id = 0
                session_start = None
                last_event_time = None

                for _, row in sorted_df.iterrows():
                    event_time = row['received_at']

                    # 第一个事件或会话超时，开始新会话
                    if (session_start is None or
                            (last_event_time and event_time - last_event_time > session_timeout)):

                        # 结束上一个会话（如果存在）
                        if session_start is not None:
                            session_key = f"{group_key}_{session_id}"
                            session_ranges[session_key] = (session_start, last_event_time)

                        # 开始新会话
                        session_id += 1
                        session_start = event_time

                    last_event_time = event_time

                # 处理最后一个会话
                if session_start is not None:
                    session_key = f"{group_key}_{session_id}"
                    session_ranges[session_key] = (session_start, last_event_time)

        except Exception as e:
            from apps.core.logger import alert_logger as logger
            logger.error(f"计算会话窗口范围失败: {str(e)}")
            return {}

        return session_ranges
