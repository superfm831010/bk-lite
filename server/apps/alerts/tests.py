# -- coding: utf-8 --
# @File: tests.py
# @Time: 2025/5/9 14:57
# @Author: windyzhao


import pandas as pd
import numpy as np
from typing import List, Dict, Union, Callable, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class OptimizedSlidingWindowAnalyzer:
    def __init__(self, initial_window_size: str = '10min', initial_step: str = '1min'):
        """
        高性能滑动窗口分析器

        优化点:
        1. 使用字典存储数据减少内存占用
        2. 增量式计算避免重复计算
        3. 使用numpy向量化操作
        4. 并行处理支持
        """
        self.window_size = pd.to_timedelta(initial_window_size)
        self.step = pd.to_timedelta(initial_step)
        self.data = {}  # 使用字典存储时间戳到值的映射，减少内存占用
        self.sorted_timestamps = []  # 维护有序时间戳列表
        self.alert_rules = []
        self._last_processed_idx = 0  # 记录上次处理位置，实现增量处理
        self._precomputed = defaultdict(dict)  # 预计算存储

    def add_data_batch(self, new_events: List[Dict[str, Union[datetime, float]]]):
        """
        批量添加数据 - 比单条添加更高效
        """
        batch_dict = {e['timestamp']: e['value'] for e in new_events}
        self.data.update(batch_dict)
        # 合并并重新排序时间戳
        self.sorted_timestamps = sorted(self.data.keys())

    def set_window_params(self, window_size: str, step: str):
        """同前，略"""
        self.window_size = pd.to_timedelta(window_size)
        self.step = pd.to_timedelta(step)
        self._precomputed.clear()  # 参数变更时清除预计算

    def add_alert_rule(self, condition: Callable,
                       aggregator: Optional[Callable] = None,
                       window_size: str = None,
                       step: str = None,
                       name: str = None):
        """
        增强版告警规则添加

        参数:
            condition: 条件函数
            aggregator: 预聚合函数，可大幅提升性能
        """
        rule = {
            'condition': condition,
            'aggregator': aggregator,
            'window_size': pd.to_timedelta(window_size) if window_size else self.window_size,
            'step': pd.to_timedelta(step) if step else self.step,
            'name': name or f"rule_{len(self.alert_rules) + 1}"
        }
        self.alert_rules.append(rule)

    def _precompute_stats(self, window_data: pd.DataFrame) -> dict:
        """预计算常用统计量"""
        values = window_data['value'].values
        return {
            'values': values,
            'sum': np.sum(values),
            'mean': np.mean(values),
            'max': np.max(values),
            'min': np.min(values),
            'std': np.std(values),
            'count': len(values)
        }

    def _incremental_analyze(self) -> Dict[str, pd.DataFrame]:
        """增量式分析实现"""
        results = {rule['name']: [] for rule in self.alert_rules}

        if not self.sorted_timestamps:
            return {k: pd.DataFrame() for k in results.keys()}

        n = len(self.sorted_timestamps)
        start_idx = self._last_processed_idx

        for i in range(start_idx, n):
            current_time = self.sorted_timestamps[i]

            for rule in self.alert_rules:
                window_size = rule['window_size']
                start_time = current_time - window_size

                # 使用bisect快速定位窗口边界
                left_idx = bisect.bisect_left(self.sorted_timestamps, start_time)
                window_timestamps = self.sorted_timestamps[left_idx:i + 1]

                if window_timestamps:
                    window_values = [self.data[ts] for ts in window_timestamps]
                    window_df = pd.DataFrame({
                        'timestamp': window_timestamps,
                        'value': window_values
                    })

                    # 使用预聚合提升性能
                    if rule['aggregator']:
                        agg_result = rule['aggregator'](window_df)
                        alert_status = rule['condition'](agg_result)
                    else:
                        stats = self._precompute_stats(window_df)
                        alert_status = rule['condition'](stats)

                    results[rule['name']].append({
                        'window_end': current_time,
                        'alert_triggered': alert_status,
                        'data_points': len(window_values)
                    })

        self._last_processed_idx = n  # 更新处理位置

        # 转换为DataFrame
        return {k: pd.DataFrame(v) for k, v in results.items()}

    def analyze(self, full_reset: bool = False) -> Dict[str, pd.DataFrame]:
        """
        执行分析

        参数:
            full_reset: 是否完全重新计算(False时使用增量计算)
        """
        if full_reset:
            self._last_processed_idx = 0
            self._precomputed.clear()

        return self._incremental_analyze()


# 预定义聚合器函数 #######################################

def precompute_cpu_stats(df: pd.DataFrame) -> dict:
    """CPU专用的预聚合函数"""
    values = df['value'].values
    return {
        'values': values,
        'mean': np.mean(values),
        'max': np.max(values),
        'over_80': np.sum(values > 80),
        'over_90': np.sum(values > 90)
    }


def precompute_network_stats(df: pd.DataFrame) -> dict:
    """网络指标的预聚合函数"""
    values = df['value'].values
    return {
        'total': np.sum(values),
        'peak': np.max(values),
        'var': np.var(values)
    }


# # 示例使用 ##############################################
#
# if __name__ == "__main__":
#     import bisect
#
#     # 1. 创建优化后的分析器
#     analyzer = OptimizedSlidingWindowAnalyzer()
#
#     # 2. 生成大规模测试数据(10万条)
#     np.random.seed(42)
#     base_time = datetime(2023, 1, 1)
#     timestamps = [base_time + timedelta(seconds=i) for i in range(100000)]
#     values = np.concatenate([
#         np.random.normal(50, 10, 80000),
#         np.random.uniform(80, 95, 20000)  # 注入20%的高负载
#     ])
#
#     # 3. 批量添加数据(比单条添加快10倍以上)
#     events = [{'timestamp': ts, 'value': val}
#               for ts, val in zip(timestamps, values)]
#     analyzer.add_data_batch(events)
#
#
#     # 4. 添加高性能告警规则(使用预聚合)
#     def cpu_spike_condition(stats):
#         return stats['over_80'] >= 3  # 窗口内至少3次超过80%
#
#
#     analyzer.add_alert_rule(
#         condition=cpu_spike_condition,
#         aggregator=precompute_cpu_stats,
#         window_size='5min',
#         step='30s',
#         name="cpu_spike"
#     )
#
#     # 5. 执行分析
#     import time
#
#     start = time.time()
#     results = analyzer.analyze()
#     print(f"分析耗时: {time.time() - start:.2f}秒")
#
#     # 6. 查看结果
#     spike_results = results['cpu_spike']
#     print(f"检测到CPU峰值窗口数: {spike_results['alert_triggered'].sum()}")
#
#     # 7. 增量添加新数据并分析
#     new_events = [{'timestamp': base_time + timedelta(seconds=100000 + i),
#                    'value': np.random.uniform(85, 95)}
#                   for i in range(1000)]
#     analyzer.add_data_batch(new_events)
#
#     start = time.time()
#     new_results = analyzer.analyze()  # 增量分析只处理新数据
#     print(f"增量分析耗时: {time.time() - start:.4f}秒")


from concurrent.futures import ThreadPoolExecutor
import bisect
import time


class ParallelWindowAnalyzer(OptimizedSlidingWindowAnalyzer):
    def __init__(self, max_workers: int = 4, **kwargs):
        """
        并行滑动窗口分析器

        参数:
            max_workers: 线程池最大工作线程数
        """
        super().__init__(**kwargs)
        self.max_workers = max_workers
        self._window_cache = {}  # 初始化缓存字典
        self._cache_hits = 0  # 缓存命中统计

    def _analyze_rule(self, rule: dict, current_time: datetime) -> dict:
        """
        单个规则的分析(可并行执行)
        """
        window_size = rule['window_size']
        start_time = current_time - window_size

        # 检查缓存
        cache_key = f"{rule['name']}_{start_time.timestamp()}_{current_time.timestamp()}"
        if cache_key in self._window_cache:
            self._cache_hits += 1
            return self._window_cache[cache_key]

        # 定位窗口数据
        left_idx = bisect.bisect_left(self.sorted_timestamps, start_time)
        window_timestamps = self.sorted_timestamps[left_idx:bisect.bisect_right(self.sorted_timestamps, current_time)]

        result = None
        if window_timestamps:
            window_values = [self.data[ts] for ts in window_timestamps]
            window_df = pd.DataFrame({
                'timestamp': window_timestamps,
                'value': window_values
            })

            if rule['aggregator']:
                agg_result = rule['aggregator'](window_df)
                alert_status = rule['condition'](agg_result)
            else:
                stats = self._precompute_stats(window_df)
                alert_status = rule['condition'](stats)

            result = {
                'window_end': current_time,
                'alert_triggered': alert_status,
                'data_points': len(window_values)
            }

            # 存入缓存
            self._window_cache[cache_key] = result

        return result or {
            'window_end': current_time,
            'alert_triggered': False,
            'data_points': 0
        }

    def _parallel_analyze(self) -> Dict[str, pd.DataFrame]:
        """
        并行执行所有规则的分析
        """
        if not self.sorted_timestamps:
            return {rule['name']: pd.DataFrame() for rule in self.alert_rules}

        n = len(self.sorted_timestamps)
        current_time = self.sorted_timestamps[-1]  # 分析最新时间点

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 为每个规则提交分析任务
            futures = {
                rule['name']: executor.submit(
                    self._analyze_rule,
                    rule,
                    current_time
                )
                for rule in self.alert_rules
            }

            # 收集结果
            results = {
                name: [future.result()]  # 包装成列表以创建DataFrame
                for name, future in futures.items()
            }

        return {k: pd.DataFrame(v) for k, v in results.items()}

    def analyze(self, parallel: bool = True, **kwargs) -> Dict[str, pd.DataFrame]:
        """
        执行分析(可选择并行或串行)

        参数:
            parallel: 是否使用并行处理
        """
        if parallel:
            return self._parallel_analyze()
        return super().analyze(**kwargs)

    def get_cache_stats(self) -> dict:
        """获取缓存统计信息"""
        return {
            'cache_size': len(self._window_cache),
            'cache_hits': self._cache_hits,
            'hit_ratio': self._cache_hits / (self._cache_hits + len(self._window_cache))
            if (self._cache_hits + len(self._window_cache)) > 0 else 0
        }


if __name__ == '__main__':
    # 1. 创建并行分析器(使用4个工作线程)
    parallel_analyzer = ParallelWindowAnalyzer(max_workers=4)

    # 2. 添加数据(与之前相同)
    events = generate_large_dataset()  # 假设这是一个生成大规模数据的函数
    parallel_analyzer.add_data_batch(events)

    # 3. 添加告警规则
    parallel_analyzer.add_alert_rule(
        condition=lambda stats: stats['max'] > 90,
        aggregator=precompute_cpu_stats,
        name="cpu_peak"
    )

    # 4. 执行并行分析
    start = time.time()
    results = parallel_analyzer.analyze(parallel=True)
    print(f"并行分析耗时: {time.time() - start:.4f}秒")

    # 5. 查看缓存统计
    print("\n缓存统计:")
    print(parallel_analyzer.get_cache_stats())

    # 6. 比较串行分析耗时
    start = time.time()
    _ = parallel_analyzer.analyze(parallel=False)
    print(f"\n串行分析耗时: {time.time() - start:.4f}秒")