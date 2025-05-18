import numpy as np
import pandas as pd
from sanic.log import logger
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
        logger.info(df)
        if freq == 'infer':
            inferred = pd.infer_freq(df.index)
            if inferred is None:
                logger.warning("无法推断频率，使用默认5min")
                inferred = '5min'
            else:
                logger.debug(f"推断频率: {inferred}")
            freq = inferred
        df = df.asfreq(freq)
        logger.info(f"时间序列频率设置为: {freq}, 样本数: {len(df)}")
        return df

    def _fill_and_generate_features(self, df: pd.DataFrame, window: int) -> pd.DataFrame:
        """
        根据时间序列填补缺失值并构造特征集合
        """
        # 保存原始索引以便后续对齐
        original_index = df.index

        df['value'] = df['value'].interpolate('linear').bfill().ffill()

        supervised = 'label' in df.columns
        if not supervised:
            df['label'] = 0  # 填充占位，方便处理无标签数据

        rolling = df['value'].rolling(window, min_periods=1)
        df['rolling_mean'] = rolling.mean()
        df['rolling_std'] = rolling.std().fillna(1e-5)  # 避免除以0

        # 构造特征集合
        df_features = {
            'value': df['value'],
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

        # 将特征转为DataFrame并合并
        features_df = pd.DataFrame(df_features, index=df.index)
        features_df['label'] = df['label']

        return features_df

    def generate_features(self, df: pd.DataFrame, freq: str = 'infer', window: int = 5) -> tuple:
        """
        生成特征并返回特征列表
        """
        logger.info(f"开始生成特征，窗口大小: {window}, 频率: {freq}")

        # 确保时间戳列的处理统一
        if 'timestamp' not in df.columns:
            if df.index.name == 'timestamp':
                df = df.reset_index()
            else:
                raise ValueError("数据必须包含timestamp列或以timestamp为索引")

        # 设置频率并填充缺失值
        df_with_freq = self._infer_and_set_freq(df, freq)
        df_features = self._fill_and_generate_features(df_with_freq, window)

        # 移除NaN值但保留索引信息
        original_length = len(df_features)
        df_features = df_features.dropna()
        if len(df_features) < original_length:
            logger.warning(
                f"特征生成过程中移除了 {original_length - len(df_features)} 条含有NaN的记录")

        # 获取特征列名
        feature_columns = [
            col for col in df_features.columns if col != 'label']

        logger.info(
            f"特征生成完成，共{len(feature_columns)}个特征，数据形状: {df_features.shape}")
        return df_features, feature_columns

    def visualize_anomaly_detection_results(self, test_df, y_pred, title="异常检测结果", output_path=None):
        """
        可视化异常检测结果并计算评估指标
        """
        if 'timestamp' in test_df.columns:
            test_df = test_df.set_index('timestamp')

        has_true_labels = 'label' in test_df.columns

        plt.figure(figsize=(15, 8))
        plt.plot(test_df.index, test_df['value'], label='原始数据')

        # 找出异常点
        anomaly_indices = np.where(y_pred == 1)[0]
        anomaly_timestamps = test_df.index[anomaly_indices]
        anomaly_values = test_df['value'].iloc[anomaly_indices]

        plt.scatter(anomaly_timestamps, anomaly_values,
                    color='red', label='检测到的异常点', zorder=5)

        if has_true_labels:
            true_anomaly_indices = np.where(test_df['label'] == 1)[0]
            true_anomaly_timestamps = test_df.index[true_anomaly_indices]
            true_anomaly_values = test_df['value'].iloc[true_anomaly_indices]
            plt.scatter(true_anomaly_timestamps, true_anomaly_values,
                        color='green', marker='x', s=100, label='真实异常点', zorder=4)

        plt.title(title)
        plt.xlabel('时间')
        plt.ylabel('数值')
        plt.legend()
        plt.grid(True)

        if output_path:
            plt.savefig(output_path)
            logger.info(f"结果图表已保存至 {output_path}")

        # 计算评估指标
        metrics = {}
        if has_true_labels:
            metrics['accuracy'] = accuracy_score(test_df['label'], y_pred)
            metrics['precision'] = precision_score(
                test_df['label'], y_pred, zero_division=0)
            metrics['recall'] = recall_score(
                test_df['label'], y_pred, zero_division=0)
            metrics['f1'] = f1_score(test_df['label'], y_pred, zero_division=0)

        return metrics

    def evaluate_model(self):
        """
        评估模型性能，返回评估指标
        """
        if not hasattr(self, 'test_data') or self.test_data is None:
            logger.warning("没有测试数据，无法评估模型")
            return {}

        X_test, y_test = self.test_data
        if not hasattr(self, 'model') or self.model is None:
            logger.warning("模型未训练，无法评估")
            return {}

        y_pred = self.model.predict(X_test)

        # 转换隔离森林等算法的结果 (-1: 异常, 1: 正常) 到 (1: 异常, 0: 正常)
        if hasattr(self, 'convert_predictions'):
            y_pred = self.convert_predictions(y_pred)

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0)
        }

        logger.info(f"模型评估结果: Accuracy={metrics['accuracy']:.4f}, "
                    f"Precision={metrics['precision']:.4f}, "
                    f"Recall={metrics['recall']:.4f}, "
                    f"F1={metrics['f1']:.4f}")

        return metrics

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        使用训练好的模型进行预测

        参数:
            data: DataFrame，包含待预测的时间序列数据

        返回:
            带有预测结果的DataFrame
        """
        if not hasattr(self, 'model') or self.model is None:
            raise ValueError("模型尚未训练或加载")

        if not hasattr(self, 'feature_columns') or not self.feature_columns:
            raise ValueError("特征列未定义")

        logger.info(f"开始预测，输入数据形状: {data.shape}")

        # 保存原始数据的副本
        original_data = data.copy()

        # 处理时间戳字段
        has_timestamp = 'timestamp' in data.columns
        if has_timestamp:
            data_with_index = data.set_index('timestamp')
        else:
            data_with_index = data

        # 从训练配置中获取窗口大小和频率
        window = self.train_config.get('window', 5)
        freq = self.train_config.get('freq', 'infer')

        # 预处理数据并生成特征
        # 注意：这里我们需要保留重设index前的数据用于对齐
        if has_timestamp:
            processed_data, _ = self.generate_features(data, freq, window)
        else:
            processed_data, _ = self.generate_features(data.reset_index().rename(
                columns={data.index.name: 'timestamp'}), freq, window)

        # 确保索引名称存在
        if processed_data.index.name is None:
            processed_data.index.name = 'timestamp'

        # 确保所有特征都存在
        missing_features = [
            f for f in self.feature_columns if f not in processed_data.columns]
        if missing_features:
            logger.warning(f"缺少特征: {missing_features}，将使用0填充")
            for f in missing_features:
                processed_data[f] = 0

        # 获取特征数据
        X = processed_data[self.feature_columns].values

        # 标准化数据(如果有标准化器)
        if hasattr(self, 'scaler') and self.scaler is not None:
            logger.info("应用特征标准化")
            X = self.scaler.transform(X)

        # 预测
        y_pred = self.model.predict(X)

        # 转换预测结果(如隔离森林算法)
        if hasattr(self, 'convert_predictions'):
            y_pred = self.convert_predictions(y_pred)

        # 创建包含预测结果的DataFrame
        prediction_df = pd.DataFrame(
            {'anomaly': y_pred}, index=processed_data.index)

        # 通过原始数据的索引进行匹配，确保数据长度一致
        # 对于未预测的数据点（如窗口前的点或缺失的点），将其anomaly值设为0
        if has_timestamp:
            # 重设索引，确保timestamp列存在
            result = original_data.copy()
            # 将预测结果匹配回原始时间戳
            result = result.set_index('timestamp')
            # 使用左连接合并预测结果
            result = result.join(prediction_df[['anomaly']], how='left')
            # 填充缺失的预测结果为0
            result['anomaly'] = result['anomaly'].fillna(0).astype(int)
            # 重设索引返回与输入相同格式
            result = result.reset_index()
        else:
            # 直接在原索引上操作
            result = original_data.copy()
            result = result.join(prediction_df[['anomaly']], how='left')
            result['anomaly'] = result['anomaly'].fillna(0).astype(int)

        anomaly_count = result['anomaly'].sum()
        logger.info(
            f"预测完成，检测到 {anomaly_count} 个异常点，占比 {anomaly_count / len(result):.2%}")

        return result
