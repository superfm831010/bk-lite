# -- coding: utf-8 --
# @File: alert_engine.py
# @Time: 2025/5/21 11:02
# @Author: windyzhao
# -- coding: utf-8 --
# @File: alert_engine.py
# @Time: 2025/5/21 11:02
# @Author: windyzhao
import pandas as pd
import numpy as np
from typing import Dict, List, Callable, Tuple, Any
from dataclasses import dataclass
import logging
import hashlib
import json

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
    alert_sources: List[str] = None
    # 聚合策略配置详解：
    aggregation_strategy: str = "group_by"
    """
    告警聚合策略，决定如何处理相似的告警：

    1. "group_by": 按指定字段分组聚合（默认）
       - 相同主机+实例+指标的告警会聚合到一个告警中
       - 例如：host1的CPU使用率高，多次触发只产生1个告警
       - 适用场景：避免同一问题产生大量重复告警

    2. "merge_all": 合并所有相同规则的告警
       - 不管主机、实例等字段，只要是同一个规则触发就合并
       - 例如：多台主机CPU都超标，合并成1个"批量CPU告警"
       - 适用场景：集群级别的告警，关注整体趋势

    3. "create_new": 总是创建新告警
       - 每次规则触发都创建独立的告警，不进行任何聚合
       - 例如：每次CPU超标都产生新告警，保留完整历史
       - 适用场景：需要详细记录每次异常的场景
    """

    aggregation_window: str = "0"
    """
    聚合时间窗口，控制告警聚合的时间范围：

    作用：
    - 只有在此时间窗口内的告警才会被聚合
    - 超过时间窗口的告警即使条件相同也不会聚合

    示例：
    - 设置为"5m"：5分钟内的相似告警会聚合
    - 设置为"1h"：1小时内的相似告警会聚合
    - 设置为"0"：禁用时间窗口限制

    实际场景：
    - CPU告警在10:00触发，10:03再次触发 → 聚合到同一告警
    - CPU告警在10:00触发，10:07再次触发 → 创建新告警（超过5分钟）

    好处：
    - 避免长时间累积过多事件到单个告警
    - 确保告警的时效性和相关性
    """

    max_alerts_per_group: int = 100
    """
    每个分组最大告警数量限制：

    作用：
    - 防止单个告警组包含过多的事件或子告警
    - 避免告警爆炸导致系统性能问题

    实际场景：
    - 网络抖动导致1000台主机同时告警
    - 限制为100，只保留最新的100个相关告警
    - 超出部分会被丢弃或创建新的告警组

    保护机制：
    - 防止单个告警包含过多数据导致查询缓慢
    - 避免告警通知包含过多信息难以阅读
    - 保护数据库和内存使用
    """


class RuleEngine:
    """高性能Pandas规则引擎（优化版：按实例分组处理）"""

    OPERATORS = {
        '>': np.greater,
        '>=': np.greater_equal,
        '<': np.less,
        '<=': np.less_equal,
        '==': np.equal
    }

    # 定义实例分组字段
    INSTANCE_GROUP_FIELDS = ['item', 'resource_id', 'resource_type', 'alert_source']

    def __init__(self, window_size: str = "10min"):
        self.window_size = pd.to_timedelta(window_size)  # 事件处理窗口
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
                is_active=rule_config.get('is_active', True),
                alert_sources=rule_config.get('alert_sources', None),
                # 新增聚合策略配置
                aggregation_strategy=rule_config.get('aggregation_strategy', 'group_by'),
                aggregation_window=rule_config.get('aggregation_window', '0'),
                max_alerts_per_group=rule_config.get('max_alerts_per_group', 100)
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
        # 创建阈值条件函数
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
        # 创建持续条件函数
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
        # 创建状态条件函数
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

    def group_events_by_instance(self, events: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        按实例分组事件数据

        Args:
            events: 原始事件DataFrame

        Returns:
            按实例指纹分组的事件字典
        """
        if events.empty:
            return {}

        # 为每个事件生成实例指纹
        events = events.copy()

        # 确保必要的字段存在
        required_fields = ['item', 'resource_id', 'resource_type', 'alert_source']
        missing_fields = [field for field in required_fields if field not in events.columns]
        if missing_fields:
            logger.warning(f"Missing required fields for grouping: {missing_fields}")
            # 为缺失的字段填充默认值
            for field in missing_fields:
                events[field] = 'unknown'

        # 生成实例指纹
        events['instance_fingerprint'] = events.apply(
            lambda row: self.generate_instance_fingerprint(row.to_dict()),
            axis=1
        )

        # 按实例指纹分组
        grouped_events = {}
        for fingerprint, group_df in events.groupby('instance_fingerprint'):
            # 重置索引以确保连续性
            clean_group = group_df.drop('instance_fingerprint', axis=1).reset_index(drop=True)

            # 确保分组不为空
            if not clean_group.empty:
                grouped_events[fingerprint] = clean_group
            else:
                logger.warning(f"Empty group found for fingerprint: {fingerprint}")

        logger.info(f"Grouped {len(events)} events into {len(grouped_events)} instances")
        return grouped_events

    def generate_instance_fingerprint(self, event_data: Dict[str, Any]) -> str:
        """
        生成实例指纹，用于标识唯一实例

        Args:
            event_data: 事件数据

        Returns:
            32位MD5哈希字符串作为实例指纹
        """
        fingerprint_data = {}

        for field in self.INSTANCE_GROUP_FIELDS:
            value = event_data.get(field)

            # 处理None值和空字符串
            if value is not None and str(value).strip():
                fingerprint_data[field] = str(value).strip()
            else:
                # 为空值提供默认值，确保指纹的一致性
                fingerprint_data[field] = 'unknown'
                logger.debug(f"Field '{field}' is empty or None, using 'unknown' as default")

        # 确保字段顺序一致
        sorted_data = json.dumps(fingerprint_data, sort_keys=True, ensure_ascii=False)
        fingerprint = hashlib.md5(sorted_data.encode('utf-8')).hexdigest()

        logger.debug(f"Generated fingerprint: {fingerprint} for data: {fingerprint_data}")
        return fingerprint

    def _check_instance_alert_status(self, instance_events: pd.DataFrame,
                                     instance_fingerprint: str,
                                     rule: AlertRule) -> Tuple[bool, List[Dict], str]:
        """
        检查实例是否已有活跃告警

        Args:
            instance_events: 实例事件数据
            instance_fingerprint: 实例指纹
            rule: 告警规则

        Returns:
            (是否需要创建新告警, 相关告警列表, 操作类型)
        """
        # 查询该实例是否已有活跃告警
        query_conditions = {
            'rule_name': rule.name,
            'status__in': ['active', 'firing', 'pending'],
            'fingerprint': instance_fingerprint,  # 使用实例指纹查询
        }

        # 添加时间窗口限制
        if rule.aggregation_window and rule.aggregation_window != "0":
            aggregation_window = pd.to_timedelta(rule.aggregation_window)
            current_time = pd.Timestamp.now()
            query_conditions['created_at__gte'] = current_time - aggregation_window

        related_alerts = self._query_alerts_from_db(query_conditions)

        if not related_alerts:
            return True, [], "create_new"
        else:
            # 已有活跃告警，更新现有告警
            return False, related_alerts, "update_existing"

    def _query_alerts_from_db(self, query_conditions: Dict) -> List[Dict]:
        """
        从数据库查询告警实例（需要根据实际的ORM模型实现）

        Args:
            query_conditions: 查询条件字典

        Returns:
            告警实例列表
        """
        # TODO: 根据实际的Django模型或其他ORM实现
        # 例如：
        # from apps.alerts.models import Alert
        # alerts = Alert.objects.filter(**query_conditions).values()
        # return list(alerts)

        # 临时返回空列表，需要调用方实现具体的数据库查询
        return []

    def _process_instance_events(self, instance_events: pd.DataFrame,
                                 instance_fingerprint: str) -> Dict[str, Dict[str, Any]]:
        """
        处理单个实例的事件

        Args:
            instance_events: 单个实例的事件数据
            instance_fingerprint: 实例指纹

        Returns:
            该实例的规则处理结果
        """
        results = {}

        for name, rule in self.rules.items():
            if not rule.is_active:
                continue

            try:
                # 对单个实例应用规则（这样保证了持续条件等规则的正确性）
                triggered, event_groups = rule.condition(instance_events)

                if triggered:
                    # 展平事件ID列表
                    flat_event_ids = [event_id for group in event_groups for event_id in group]

                    # 检查是否需要创建新告警（基于实例指纹）
                    should_create_new, related_alerts, operation_type = self._check_instance_alert_status(
                        instance_events, instance_fingerprint, rule
                    )

                    results[name] = {
                        'triggered': True,
                        'event_ids': flat_event_ids,
                        'instance_fingerprint': instance_fingerprint,
                        'instance_events': instance_events,
                        'severity': rule.severity,
                        'description': rule.description,
                        'rule': rule,
                        'should_create_new': should_create_new,
                        'related_alerts': related_alerts,
                        'operation_type': operation_type,
                    }
                else:
                    results[name] = {'triggered': False}

            except Exception as e:
                logger.error(f"Rule {name} evaluation failed for instance {instance_fingerprint}: {e}")
                results[name] = {'triggered': False, 'error': str(e)}

        return results

    def process_events(self, events: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        处理事件并返回告警结果（按实例分组处理）
        """
        if events.empty:
            return {}

        # 修复时间处理逻辑
        events = events.copy()

        # 确保 received_at 是 datetime 类型，而不是 timedelta
        if 'received_at' in events.columns:
            events['received_at'] = pd.to_datetime(events['received_at'])
            # 只保留窗口内的数据
            window_end = events['received_at'].max()
            events = events[events['received_at'] >= (window_end - self.window_size)]
        else:
            logger.warning("'received_at' column not found in events DataFrame")

        # 确保存在alert_source字段
        events['alert_source'] = events['source__name']

        # **关键：按实例分组处理**
        grouped_events = self.group_events_by_instance(events)

        if not grouped_events:
            logger.info("No events to process after grouping")
            return {}

        results = {}

        # 对每个实例分别应用规则
        for instance_fingerprint, instance_events in grouped_events.items():
            logger.debug(f"Processing {len(instance_events)} events for instance: {instance_fingerprint}")

            instance_results = self._process_instance_events(instance_events, instance_fingerprint)

            # 合并结果
            for rule_name, rule_result in instance_results.items():
                if rule_name not in results:
                    results[rule_name] = {
                        'triggered': False,
                        'instances': {},
                        'total_event_ids': [],
                        'severity': None,
                        'description': None,
                    }

                if rule_result['triggered']:
                    results[rule_name]['triggered'] = True
                    results[rule_name]['instances'][instance_fingerprint] = rule_result
                    results[rule_name]['total_event_ids'].extend(rule_result['event_ids'])
                    results[rule_name]['severity'] = rule_result['severity']
                    results[rule_name]['description'] = rule_result['description']

        logger.info(f"Processing completed. {len(results)} rules triggered.")
        return results

    def test_demonstrate_aggregation_strategies(self):
        """
        演示不同聚合策略的效果（仅用于说明，实际不会调用）
        """
        # 假设场景：3台主机的CPU使用率都超过80%
        events_example = """
        host1, cpu.usage, 85%, 10:00:00
        host2, cpu.usage, 90%, 10:00:30  
        host3, cpu.usage, 87%, 10:01:00
        host1, cpu.usage, 88%, 10:02:00  # 同一主机再次触发
        """

        # 现在按实例分组后的处理：
        # 实例1: (item=cpu.usage, resource_id=host1, ...)
        # 实例2: (item=cpu.usage, resource_id=host2, ...)
        # 实例3: (item=cpu.usage, resource_id=host3, ...)

        # 每个实例独立处理规则，确保持续条件等规则的正确性
        # 每个实例最多产生一个告警（基于实例指纹去重）

        pass
