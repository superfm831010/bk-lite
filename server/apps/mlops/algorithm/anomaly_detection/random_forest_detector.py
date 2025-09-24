from sklearn.ensemble import RandomForestClassifier
from apps.mlops.algorithm.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection
from hyperopt import hp
import pandas as pd
import numpy as np


class RandomForestAnomalyDetector(BaseAnomalyDetection):
    # def get_default_hyperopt_config(self):
    #     return {
    #         "n_estimators": hp.randint("n_estimators", 100, 500),
    #         "max_depth": hp.randint("max_depth", 10, 50),
    #         "min_samples_split": hp.randint("min_samples_split", 2, 10),
    #         "min_samples_leaf": hp.randint("min_samples_leaf", 1, 5),
    #         "max_features": hp.choice("max_features", ["sqrt", "log2", None]),
    #         "bootstrap": hp.choice("bootstrap", [True, False]),
    #         "class_weight": hp.choice("class_weight", ["balanced", "balanced_subsample", None]),
    #     }
        
    def build_model(self, train_params):
        model = RandomForestClassifier(**train_params)
        return model
    
    def _predict_without_resampling(self, data: pd.DataFrame, model) -> pd.DataFrame:
        """
        不进行频率重采样的预测方法，避免数据扩展问题
        
        Args:
            data: 包含timestamp和value列的DataFrame
            model: 已训练的模型
            
        Returns:
            包含预测结果的DataFrame，长度与输入数据相同
        """
        from apps.core.logger import mlops_logger as logger
        
        logger.info(f"使用无重采样预测方法，输入数据长度: {len(data)}")
        
        # 复制数据避免修改原始数据
        df = data.copy()
        
        # 确保timestamp列转换为datetime格式
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.set_index('timestamp')
        
        # 获取模型的窗口大小
        windows_size = getattr(model, 'window', 10)  # 默认窗口大小为10
        
        logger.info(f"模型窗口大小: {windows_size}")
        
        # 计算滚动窗口统计量，但不进行频率重采样
        rolling = df['value'].rolling(windows_size, min_periods=1)
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
            'autocorr_1': df['value'].rolling(windows_size * 2, min_periods=windows_size)
            .apply(lambda x: x.autocorr(lag=1) if len(x) > windows_size else 0)
            if len(df) >= windows_size * 2 else pd.Series(0, index=df.index),

            # 时间特征
            'hour': df.index.hour,
            'minute': df.index.minute,
            'dayofweek': df.index.dayofweek,
            'month': df.index.month,
            'is_weekend': (df.index.dayofweek >= 5).astype(int),
        }

        features_df = pd.DataFrame(df_features, index=df.index)
        
        # 移除NaN值
        features_df = features_df.dropna()
        
        logger.info(f"特征处理后数据长度: {len(features_df)}")
        
        # 获取特征列（排除label列）
        feature_columns = [col for col in features_df.columns if col != 'label']
        
        # 进行预测
        probabilities = model.predict_proba(features_df[feature_columns])[:, 1]
        
        result_df = pd.DataFrame({
            'value': features_df['value'],
            'anomaly_probability': probabilities,
        })
        
        logger.info(f"预测结果长度: {len(result_df)}")
        
        return result_df