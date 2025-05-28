# -- coding: utf-8 --
# @File: alert_engine.py
# @Time: 2025/5/21 11:02
# @Author: windyzhao
import pandas as pd
import numpy as np
from typing import Dict, List, Callable, Tuple, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class AlertRule:
    name: str
    condition: Callable[[pd.DataFrame], Tuple[bool, List[str]]]
    aggregation: Dict[str, List[str]]
    description: str
    title: str = ""
    content: str = ""
    severity: str = "medium"
    is_active: bool = True


class RuleEngine:
    """高性能Pandas规则引擎（优化版：全部基于原始事件窗口判断）"""

    OPERATORS = {
        '>': np.greater,
        '>=': np.greater_equal,
        '<': np.less,
        '<=': np.less_equal,
        '==': np.equal
    }

    def __init__(self, window_size: str = "10min"):
        self.window_size = pd.to_timedelta(window_size)
        self.rules: Dict[str, AlertRule] = {}

    def add_rule(self, rule_config: dict):
        try:
            condition_func = self._create_condition(rule_config)
            self.rules[rule_config['name']] = AlertRule(
                name=rule_config['name'],
                title=rule_config.get('title', ''),
                content=rule_config.get('content', ''),
                condition=condition_func,
                aggregation=rule_config.get('aggregation', {}),
                description=rule_config.get('description', ''),
                severity=rule_config.get('severity', 'medium'),
                is_active=rule_config.get('is_active', True)
            )
        except Exception as e:
            logger.error(f"Rule {rule_config.get('name')} add failed: {e}")
            raise

    def _create_condition(self, rule_config: dict) -> Callable:
        condition_type = rule_config['condition']['type']
        config = rule_config['condition']

        if condition_type == 'threshold':
            return self._create_threshold_condition(config)
        elif condition_type == 'sustained':
            return self._create_sustained_condition(config)
        elif condition_type == 'trend':
            return self._create_trend_condition(config)
        elif condition_type == 'prev_field_equals':
            return self._create_status_condition(config)
        else:
            raise ValueError(f"Unknown condition type: {condition_type}")

    def _create_threshold_condition(self, config: dict) -> Callable:
        field = config['field']
        threshold = config['threshold']
        op_func = self.OPERATORS[config['operator']]

        def condition(df: pd.DataFrame) -> Tuple[bool, List[List[str]]]:
            if df.empty:
                return False, []
            # 只取 item=field 的行
            field_df = df[df["item"] == field]
            if field_df.empty:
                return False, []
            mask = op_func(field_df["value"], threshold)
            # 将每个触发事件ID作为单独的组返回
            event_groups = [[event_id] for event_id in field_df.loc[mask, 'event_id'].tolist()]
            return len(event_groups) > 0, event_groups

        return condition

    def _create_sustained_condition(self, config: dict) -> Callable:
        field = config['field']
        threshold = config['threshold']
        op_func = self.OPERATORS[config['operator']]
        consecutive = config['required_consecutive']

        def condition(df: pd.DataFrame) -> Tuple[bool, List[List[str]]]:
            field_df = df[df["item"] == field].sort_values('received_at')
            if len(field_df) < consecutive:
                return False, []

            # 计算每个点是否满足条件
            mask = op_func(field_df["value"], threshold)

            # 寻找连续满足条件的组
            event_groups = []
            current_group = []

            # 遍历数据帧中的每一行
            for idx, row in field_df.iterrows():
                if mask[idx]:
                    # 如果满足条件，添加到当前组
                    current_group.append(row['event_id'])
                else:
                    # 不满足条件，检查之前的组是否达到了连续阈值
                    if len(current_group) >= consecutive:
                        event_groups.append(current_group)
                    # 重置当前组
                    current_group = []

            # 检查循环结束后最后一个分组
            if len(current_group) >= consecutive:
                event_groups.append(current_group)

            return len(event_groups) > 0, event_groups

        return condition

    def _create_trend_condition(self, config: dict) -> Callable:
        field = config['field']
        threshold = config['threshold']
        op_func = self.OPERATORS[config['operator']]
        baseline_window = config['baseline_window']
        method = config.get('trend_method', 'absolute')

        def condition(df: pd.DataFrame) -> Tuple[bool, List[List[str]]]:
            field_df = df[df["item"] == field]
            if len(field_df) <= baseline_window:
                return False, []
            baseline = field_df["value"].iloc[:-1].rolling(baseline_window).mean().iloc[-1]
            current = field_df["value"].iloc[-1]
            if method == 'percentage':
                change = (current - baseline) / baseline * 100 if baseline != 0 else 0
            else:
                change = current - baseline

            # 检查是否满足条件
            triggered = op_func(change, threshold)

            # 创建事件组列表
            event_groups = []
            if triggered:
                # 获取最新事件ID作为触发事件
                latest_event_id = field_df['event_id'].iloc[-1]
                event_groups.append([latest_event_id])

            return len(event_groups) > 0, event_groups

        return condition

    def _create_status_condition(self, config: dict) -> Callable:
        group_fields = config['group_by']
        status_field = config['prev_status_field']
        target_status = config['prev_status_value']

        def condition(df: pd.DataFrame) -> Tuple[bool, List[List[str]]]:
            if len(df) < 2:
                return False, []
            df_sorted = df.sort_values('received_at')
            df_sorted = df_sorted[df_sorted[status_field] == target_status]
            grouped = df_sorted.groupby(group_fields)
            event_groups = []
            for _, group in grouped:
                if len(group) < 2:
                    continue
                prev_status = group[status_field].iloc[-2]
                if prev_status == target_status:
                    # 每个触发事件作为独立的组
                    event_groups.append([group['event_id'].iloc[-1]])
            return len(event_groups) > 0, event_groups

        return condition

    def process_events(self, events: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        处理事件并返回告警结果
        返回格式: {rule_name: {'triggered': bool, 'event_ids': List[str], ...}}
        """
        if events.empty:
            return {}

        # 只保留窗口内的数据
        events = events.copy()
        events['received_at'] = pd.to_datetime(events['received_at'])
        window_end = events['received_at'].max()
        events = events[events['received_at'] >= (window_end - self.window_size)]

        results = {}
        for name, rule in self.rules.items():
            if not rule.is_active:
                continue
            try:
                triggered, event_ids = rule.condition(events)
                results[name] = {
                    'triggered': triggered,
                    'event_ids': event_ids,
                    'severity': rule.severity,
                    'description': rule.description,
                    'rule': rule,
                }
            except Exception as e:
                logger.error(f"Rule {name} evaluation failed: {e}")
                results[name] = {'triggered': False, 'error': str(e)}

        return results
