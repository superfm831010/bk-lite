import numpy as np
import pandas as pd
from loguru import logger
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class BaseAnomalyDetection:
    def load_csv_data(self, csv_file: str) -> pd.DataFrame:
        """
        加载CSV数据文件，并确保数据按时间排序
        """
        logger.info(f"加载数据文件: {csv_file}")
        df = pd.read_csv(csv_file, parse_dates=['timestamp'])
        df = df.dropna(subset=['timestamp', 'value'])
        return df.sort_values('timestamp')

    def _infer_and_set_freq(self, df: pd.DataFrame, freq: str) -> pd.DataFrame:
        """
        推断时间序列数据的频率，如果无法推断则使用默认频率
        """
        df = df.set_index('timestamp')
        if freq == 'infer':
            inferred = pd.infer_freq(df.index)
            if inferred is None:
                logger.warning("无法推断频率，使用默认5min")
                inferred = '5min'
            else:
                logger.debug(f"推断频率: {inferred}")
            freq = inferred
        return df.asfreq(freq)

    def _fill_and_generate_features(self, df: pd.DataFrame, window: int) -> pd.DataFrame:
        """
        根据时间序列填补缺失值并构造特征集合
        """
        df['value'] = df['value'].interpolate('linear').bfill().ffill()

        supervised = 'label' in df.columns
        if not supervised:
            df['label'] = 0  # 填充占位，方便处理无标签数据

        rolling = df['value'].rolling(window, min_periods=1)
        df['rolling_mean'] = rolling.mean()
        df['rolling_std'] = rolling.std().fillna(1e-5)  # 避免除以0

        # 构造特征集合
        df_features = {
            'rolling_min': rolling.min(),
            'rolling_max': rolling.max(),
            'rolling_median': rolling.median(),
            'diff_1': df['value'].diff().fillna(0),
            'diff_2': df['value'].diff().diff().fillna(0),
            'zscore': (df['value'] - df['rolling_mean']) / df['rolling_std'],
            'trend': rolling.apply(lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0),
            'autocorr_1': df['value'].rolling(window * 2, min_periods=window)
            .apply(lambda x: x.autocorr(lag=1) if len(x) > window else 0)
            if len(df) >= window * 2 else pd.Series(0, index=df.index),
            'hour': df.index.hour,
            'minute': df.index.minute,
            'dayofweek': df.index.dayofweek,
            'month': df.index.month,
            'is_weekend': (df.index.dayofweek >= 5).astype(int),
        }

        for name, values in df_features.items():
            df[name] = values

        # 如果不是有监督数据，则移除填充的`label`占位列
        if not supervised:
            df = df.drop(columns=['label'])

        return df.fillna(0).reset_index(), list(df_features.keys())

    def generate_features(self, df: pd.DataFrame, freq: str = 'infer', window: int = 12) -> (pd.DataFrame, list):
        """
        按指定频率对时间序列数据生成特征
        """
        df = self._infer_and_set_freq(df, freq)
        return self._fill_and_generate_features(df, window)

    def visualize_anomaly_detection_results(
            self,
            test_df: pd.DataFrame,
            y_pred: np.ndarray,
            title: str = "异常检测结果",
            output_path: str = "./test_results/anomaly_detection_result.png",
    ) -> dict:
        """
        可视化异常检测结果，并返回性能指标。
        """
        # 字体设置（兼容mac）
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False

        offset = getattr(self, "train_config", {}).get("window_offset", 0)
        y_true = test_df.get("label", pd.Series(0, index=test_df.index)).values.astype(int)

        full_pred = np.zeros(len(test_df), dtype=int)
        valid_len = min(len(y_pred), len(test_df) - offset)
        full_pred[offset:offset + valid_len] = y_pred[:valid_len]

        # 绘图
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(test_df["timestamp"], test_df["value"], label="时序数据")

        # 标记点
        ax.scatter(test_df["timestamp"][full_pred == 1],
                   test_df["value"][full_pred == 1],
                   color="red", label="预测异常点", s=50)

        if y_true.sum() > 0:
            ax.scatter(test_df["timestamp"][y_true == 1],
                       test_df["value"][y_true == 1],
                       color="green", marker='x', label="实际异常点", s=80)

        # 指标计算
        metrics = {
            "accuracy": accuracy_score(y_true[offset:offset + valid_len], y_pred[:valid_len]),
            "precision": precision_score(y_true[offset:offset + valid_len], y_pred[:valid_len], zero_division=0),
            "recall": recall_score(y_true[offset:offset + valid_len], y_pred[:valid_len], zero_division=0),
            "f1": f1_score(y_true[offset:offset + valid_len], y_pred[:valid_len], zero_division=0),
        }

        metrics_text = (
            f'准确率: {metrics["accuracy"]:.3f}\n'
            f'精确率: {metrics["precision"]:.3f}\n'
            f'召回率: {metrics["recall"]:.3f}\n'
            f'F1分数: {metrics["f1"]:.3f}'
        )
        ax.text(0.02, 0.98, metrics_text, transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.8), verticalalignment='top', fontsize=10)

        ax.set(title=title, xlabel="时间", ylabel="值")
        ax.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

        logger.info(f"图像保存至: {output_path}")
        logger.info(
            f"性能: Precision={metrics['precision']:.4f}, Recall={metrics['recall']:.4f}, F1={metrics['f1']:.4f}")

        return metrics
