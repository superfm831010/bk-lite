import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def generate_test_data_with_indices(num_points=None):
    """
    生成高级模拟的测试数据并返回异常索引
    """
    if num_points is None:
        num_points = 24 * 60  # 默认模拟一天（一分钟一个数据点）

    # 生成时间戳
    timestamps = [datetime(2024, 1, 2) + timedelta(minutes=i)
                  for i in range(num_points)]

    # 正常基线值
    base = 30
    period1, period2, period3 = 24 * 60, 60, 300
    cycle = (
            10 * np.sin(2 * np.pi * np.arange(num_points) / period1) +
            7 * np.sin(2 * np.pi * np.arange(num_points) / period2) +
            3 * np.sin(2 * np.pi * np.arange(num_points) / period3)
    )
    noise = np.random.normal(0, 7, size=num_points)
    values = base + cycle + noise
    values = np.clip(values, 0, 100)

    labels = np.zeros(num_points, dtype=int)  # 初始化标签

    # 异常类型索引记录
    anomaly_indices = []

    # 边界异常
    borderline_indices = np.random.choice(num_points, size=20, replace=False)
    values[borderline_indices] += np.random.uniform(10, 15, size=20)
    labels[borderline_indices] = 1
    anomaly_indices.extend(borderline_indices.tolist())

    # 过渡型异常
    transition_start = np.random.choice(list(set(range(100, num_points - 30))), size=5, replace=False)
    for start in transition_start:
        values[start:start + 30] = np.linspace(30, 80, 30)
        labels[start:start + 30] = 1
        anomaly_indices.extend(range(start, start + 30))

    # 隐匿峰值
    hidden_spike_indices = np.random.choice(list(set(range(100, num_points))), size=15, replace=False)
    values[hidden_spike_indices] = np.random.uniform(70, 80, size=15)
    labels[hidden_spike_indices] = 1
    anomaly_indices.extend(hidden_spike_indices.tolist())

    # 周期性抖动
    jitter_start = np.random.choice(list(set(range(100, num_points - 20))), size=8, replace=False)
    for start in jitter_start:
        jitter_vals = base + np.random.choice([20, 60], size=10)
        values[start:start + 10] = jitter_vals
        labels[start:start + 10] = 1
        anomaly_indices.extend(range(start, start + 10))

    # 持续微小波动
    subtle_wave_start = np.random.choice(list(set(range(100, num_points - 50))), size=8, replace=False)
    for start in subtle_wave_start:
        subtle_wave = base + 5 * np.cos(2 * np.pi * np.arange(50) / 25) + np.random.normal(0, 2, size=50)
        values[start:start + 50] = subtle_wave
        labels[start:start + 50] = 1
        anomaly_indices.extend(range(start, start + 50))

    # 干扰型异常
    intermittent_anomalies = np.random.choice(list(set(range(100, num_points))), size=12, replace=False)
    values[intermittent_anomalies] = np.random.uniform(50, 90, size=12)
    labels[intermittent_anomalies] = 1
    anomaly_indices.extend(intermittent_anomalies.tolist())

    anomaly_indices = sorted(set(anomaly_indices))  # 去重并排序
    return pd.DataFrame({"timestamp": timestamps, "value": values, "label": labels}), anomaly_indices


def generate_training_data(num_points=None, supervised: bool = True):
    """
    生成模拟的CPU训练数据，可选择是否提供异常标签（有监督或无监督）

    参数:
        num_points: 数据点数量（默认一天，每分钟一个点）
        supervised: 是否生成有监督数据（即返回标签列）

    返回:
        pd.DataFrame，包含 timestamp、value（若 supervised=True 还包含 label）
    """
    if num_points is None:
        num_points = 24 * 60  # 默认模拟一天（一分钟一个数据点）

    timestamps = [datetime(2024, 1, 1) + timedelta(minutes=i) for i in range(num_points)]

    base = 30
    period1 = 24 * 60
    period2 = 60
    cycle = (
            10 * np.sin(2 * np.pi * np.arange(num_points) / period1) +
            5 * np.sin(2 * np.pi * np.arange(num_points) / period2)
    )
    noise = np.random.normal(0, 5, size=num_points)
    values = np.clip(base + cycle + noise, 0, 100)

    labels = np.zeros(num_points, dtype=int)

    # 1. 过载峰值（Spike Load）
    spike_indices = np.random.choice(num_points, size=30, replace=False)
    values[spike_indices] = np.random.uniform(90, 100, size=30)
    labels[spike_indices] = 1

    # 2. 空转低负载（Idle Load）
    idle_indices = np.random.choice(list(set(range(num_points)) - set(spike_indices)), size=20, replace=False)
    values[idle_indices] = np.random.uniform(0, 5, size=20)
    labels[idle_indices] = 1

    # 3. 高频抖动异常（Cyclic Anomalies）
    jitter_start = np.random.choice(list(set(range(100, num_points - 20)) - set(spike_indices) - set(idle_indices)),
                                    size=10, replace=False)
    for start in jitter_start:
        values[start:start + 10] = base + np.random.choice([10, 90], size=10)
        labels[start:start + 10] = 1

    # 4. 缓慢上升异常（Slow Rise）
    rise_start = np.random.choice(list(set(range(100, num_points - 30)) - set(spike_indices) - set(idle_indices)),
                                  size=8, replace=False)
    for start in rise_start:
        values[start:start + 15] = np.linspace(40, 90, 15)
        labels[start:start + 15] = 1

    # 5. 阶跃增加（Step Increase）
    step_start = np.random.choice(list(set(range(100, num_points - 50)) - set(spike_indices) - set(idle_indices)),
                                  size=5, replace=False)
    for start in step_start:
        values[start:start + 20] = np.concatenate([np.full(10, 30), np.full(10, 80)])
        labels[start:start + 20] = 1

    # 6. 长时间高负载（Constant High）
    high_start = np.random.choice(list(set(range(num_points - 60)) - set(spike_indices) - set(idle_indices)),
                                  size=5, replace=False)
    for start in high_start:
        values[start:start + 60] = np.random.uniform(85, 95, 60)
        labels[start:start + 60] = 1

    # 7. 长时间低负载（Constant Low）
    low_start = np.random.choice(list(set(range(num_points - 60)) - set(spike_indices) - set(idle_indices)),
                                 size=5, replace=False)
    for start in low_start:
        values[start:start + 60] = np.random.uniform(5, 10, 60)
        labels[start:start + 60] = 1

    if supervised:
        return pd.DataFrame({
            "timestamp": timestamps,
            "value": values,
            "label": labels
        })
    else:
        return pd.DataFrame({
            "timestamp": timestamps,
            "value": values
        })
