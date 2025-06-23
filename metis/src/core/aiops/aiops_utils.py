from typing import Dict

import mlflow
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sanic.log import logger


class AiopsUtils:
    @classmethod
    def log_importance_features(cls, model, feature_columns):
        if hasattr(model, 'feature_importances_'):
            feature_importance = dict(
                zip(feature_columns, model.feature_importances_))
            top_features = sorted(feature_importance.items(
            ), key=lambda x: x[1], reverse=True)[:10]
            for feat, importance in top_features:
                mlflow.log_metric(f"feature_importance_{feat}", importance)

    @classmethod
    def calculate_metrics(cls, y_true: np.ndarray, y_pred: np.ndarray, subprefix: str) -> Dict[str, float]:
        """计算分类评估指标"""
        return {
            f"{subprefix}_accuracy": accuracy_score(y_true, y_pred),
            f"{subprefix}_precision": precision_score(y_true, y_pred, zero_division=0),
            f"{subprefix}_recall": recall_score(y_true, y_pred, zero_division=0),
            f"{subprefix}_f1": f1_score(y_true, y_pred, zero_division=0),
        }

    @classmethod
    def load_timestamp_csv_data(cls, csv_file: str) -> pd.DataFrame:
        df = pd.read_csv(csv_file, parse_dates=['timestamp'])
        df = df.dropna(subset=['timestamp', 'value'])
        return df.sort_values('timestamp')

    @classmethod
    def prepare_timestamp_features(cls, df: pd.DataFrame,
                                   freq: str = 'infer', window: int = 5) -> pd.DataFrame:
        df = df.set_index('timestamp')

        if freq == 'infer':
            freq = pd.infer_freq(df.index)
        df = df.asfreq(freq)

        df['value'] = df['value'].interpolate('linear').bfill().ffill()

        # 计算滚动窗口统计量
        rolling = df['value'].rolling(window, min_periods=1)
        df['rolling_mean'] = rolling.mean()
        df['rolling_std'] = rolling.std().fillna(1e-5)  # 避免除以0

        df_features = {
            # 原始值
            'value': df['value'],

            # 统计特征
            'rolling_min': rolling.min(),
            'rolling_max': rolling.max(),
            'rolling_median': rolling.median(),

            # 差分特征
            'diff_1': df['value'].diff().fillna(0),
            'diff_2': df['value'].diff().diff().fillna(0),

            # 归一化特征
            'zscore': (df['value'] - df['rolling_mean']) / df['rolling_std'],

            # 趋势特征
            'trend': rolling.apply(lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0),

            # 自相关特征
            'autocorr_1': df['value'].rolling(window * 2, min_periods=window)
            .apply(lambda x: x.autocorr(lag=1) if len(x) > window else 0)
            if len(df) >= window * 2 else pd.Series(0, index=df.index),

            # 时间特征
            'hour': df.index.hour,
            'minute': df.index.minute,
            'dayofweek': df.index.dayofweek,
            'month': df.index.month,
            'is_weekend': (df.index.dayofweek >= 5).astype(int),
        }

        features_df = pd.DataFrame(df_features, index=df.index)

        if 'label' in df.columns:
            features_df['label'] = df['label']

        features_df = features_df.dropna()

        feature_columns = [
            col for col in features_df.columns if col != 'label']
        return features_df, feature_columns

    @classmethod
    def split_timestamp_train_data(cls, X: np.ndarray, y: np.ndarray,
                                   test_size: float = 0.2, val_size: float = 0.1, random_state: int = 42):
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=random_state
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val, test_size=val_size / (1 - test_size),
            stratify=y_train_val, random_state=random_state
        )
        return X_train, X_val, X_test, y_train, y_val, y_test

    @classmethod
    def timestamp_standardize_features(cls, X_train: np.ndarray, X_val: np.ndarray = None, X_test: np.ndarray = None):

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        X_test_scaled = scaler.transform(X_test)

        return X_train_scaled, X_val_scaled, X_test_scaled
