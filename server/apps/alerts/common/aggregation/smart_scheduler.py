# -- coding: utf-8 --
# @File: smart_scheduler.py
# @Time: 2025/1/15 10:00
# @Author: windyzhao

import re
from typing import List, Dict, Any

from django.conf import settings
from django.utils import timezone

from apps.alerts.models import CorrelationRules
from apps.core.logger import alert_logger as logger


class SmartWindowScheduler:
    """智能窗口调度器 - 动态判断当前时间应该执行哪些窗口规则"""

    def __init__(self):
        self.current_time = timezone.now()

    def should_execute_fixed_window(self, window_size: str, alignment: str = 'minute') -> bool:
        """
        判断固定窗口是否应该在当前时间执行
        
        Args:
            window_size: 窗口大小，如"5min", "10min", "1h", "12min"
            alignment: 对齐方式，minute/hour/day
            
        Returns:
            bool: 是否应该执行
        """
        if settings.DEBUG:
            return True  # 在调试模式下总是执行

        try:
            # 解析窗口大小为分钟数
            window_minutes = self._parse_window_size_to_minutes(window_size)

            if alignment == 'minute':
                # 按分钟对齐：检查当前分钟是否是窗口大小的倍数
                current_minute = self.current_time.minute
                return current_minute % window_minutes == 0

            elif alignment == 'hour':
                # 按小时对齐：检查当前小时是否是窗口大小（小时）的倍数，且分钟为0
                if self.current_time.minute != 0:
                    return False
                window_hours = window_minutes // 60
                current_hour = self.current_time.hour
                return current_hour % window_hours == 0

            elif alignment == 'day':
                # 按天对齐：检查是否是午夜0点
                return (self.current_time.hour == 0 and
                        self.current_time.minute == 0)

            else:
                logger.warning(f"未知的对齐方式: {alignment}")
                return False

        except Exception as e:
            logger.error(f"判断固定窗口执行时间失败: {str(e)}")
            return False

    def _parse_window_size_to_minutes(self, window_size: str) -> int:
        """
        将窗口大小字符串转换为分钟数
        
        Args:
            window_size: 如"5min", "10min", "1h", "12min"
            
        Returns:
            int: 分钟数
        """
        # 使用正则表达式解析
        pattern = r'^(\d+)(min|h|d|s)$'
        match = re.match(pattern, window_size.lower())

        if not match:
            raise ValueError(f"无法解析窗口大小: {window_size}")

        value, unit = match.groups()
        value = int(value)

        if unit == 'min':
            return value
        elif unit == 'h':
            return value * 60
        elif unit == 'd':
            return value * 24 * 60
        elif unit == 's':
            return max(1, value // 60)  # 秒转分钟，最少1分钟
        else:
            raise ValueError(f"不支持的时间单位: {unit}")

    def get_executable_rules(self) -> Dict[str, List[CorrelationRules]]:
        """
        获取当前时间应该执行的规则，按窗口类型分组
        
        Returns:
            Dict[str, List[CorrelationRules]]: 按窗口类型分组的规则列表
        """
        executable_rules = {
            'sliding': [],
            'fixed': [],
            'session': []
        }

        # 获取所有激活的关联规则
        active_rules = CorrelationRules.objects.filter(
            aggregation_rules__is_active=True
        ).distinct().prefetch_related('aggregation_rules')

        for rule in active_rules:
            window_type = rule.window_type

            if window_type == 'sliding':
                # 滑动窗口：每分钟都执行
                executable_rules['sliding'].append(rule)

            elif window_type == 'fixed':
                # 固定窗口：检查是否应该在当前时间执行
                if self.should_execute_fixed_window(rule.window_size, rule.alignment):
                    executable_rules['fixed'].append(rule)

            elif window_type == 'session':
                # 会话窗口：根据超时时间判断执行频率
                # if self._should_execute_session_window(rule.session_timeout):
                executable_rules['session'].append(rule)

        return executable_rules

    def _should_execute_session_window(self, session_timeout: str) -> bool:
        """
        判断会话窗口是否应该执行
        
        会话窗口执行策略修正：
        - 会话窗口应该更频繁地执行以便及时处理事件分配和会话管理
        - 建议频率：每分钟执行一次，确保及时响应
        - 清理任务和告警生成可以在定时任务中处理
        
        Args:
            session_timeout: 会话超时时间，如"5min"
            
        Returns:
            bool: 是否应该执行
        """
        try:
            # 修复：会话窗口应该更频繁执行以确保及时处理
            # 每分钟都执行，确保事件能及时分配到会话中
            return True  # 总是执行，保证实时性
            
            # 如果需要降低频率，可以使用以下逻辑：
            # timeout_minutes = self._parse_window_size_to_minutes(session_timeout)
            # check_interval = max(1, min(5, timeout_minutes // 5))  # 最多5分钟间隔
            # current_minute = self.current_time.minute
            # return current_minute % check_interval == 0

        except Exception as e:
            logger.error(f"判断会话窗口执行时间失败: {str(e)}")
            return True  # 出现错误时也执行，确保系统稳定性

    def get_execution_summary(self) -> Dict[str, Any]:
        """
        获取执行摘要信息，用于日志记录
        
        Returns:
            Dict[str, Any]: 执行摘要
        """
        executable_rules = self.get_executable_rules()

        return {
            'current_time': self.current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'sliding_rules_count': len(executable_rules['sliding']),
            'fixed_rules_count': len(executable_rules['fixed']),
            'session_rules_count': len(executable_rules['session']),
            'total_executable_rules': sum(len(rules) for rules in executable_rules.values()),
            'sliding_rules': [rule.name for rule in executable_rules['sliding']],
            'fixed_rules': [
                f"{rule.name}({rule.window_size},{rule.alignment})"
                for rule in executable_rules['fixed']
            ],
            'session_rules': [
                f"{rule.name}({rule.session_timeout})"
                for rule in executable_rules['session']
            ]
        }


def create_smart_scheduler() -> SmartWindowScheduler:
    """创建智能调度器实例"""
    return SmartWindowScheduler()
