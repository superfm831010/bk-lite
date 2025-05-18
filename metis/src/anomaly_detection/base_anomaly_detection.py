"""
异常检测基础模块

提供时间序列异常检测的通用功能，包括数据处理、特征生成、模型训练与评估等
"""
import os
import abc
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any, List, Tuple, Optional, Union
from sanic.log import logger
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class BaseAnomalyDetection(abc.ABC):
    """
    异常检测基类，定义通用接口和共享功能

    实现了模板方法模式，子类只需实现特定的算法相关方法
    """

    def __init__(self):
        """初始化检测器，设置基本状态"""
        self.feature_columns = []
        self.train_config = {}
        self.model = None
        self.train_data = None
        self.val_data = None
        self.test_data = None
        self.scaler = None

    def load_csv_data(self, csv_file: str) -> pd.DataFrame:
        """
        加载CSV数据文件，并确保数据按时间排序

        参数:
            csv_file: CSV文件路径

        返回:
            处理后的DataFrame
        """
        logger.info(f"加载数据文件: {csv_file}")
        df = pd.read_csv(csv_file, parse_dates=['timestamp'])
        df = df.dropna(subset=['timestamp', 'value'])
        return df.sort_values('timestamp')

    def _infer_and_set_freq(self, df: pd.DataFrame, freq: str) -> pd.DataFrame:
        """
        推断时间序列数据的频率，如果无法推断则使用默认频率

        参数:
            df: 包含时间戳的DataFrame
            freq: 频率设置，'infer'表示自动推断

        返回:
            设置了频率的DataFrame
        """
        df = df.set_index('timestamp')

        if freq == 'infer':
            inferred = pd.infer_freq(df.index)
            if inferred is None:
                logger.warning("无法推断频率，使用默认5min")
                inferred = '5min'
            else:
                logger.info(f"推断频率: {inferred}")
            freq = inferred

        df = df.asfreq(freq)
        logger.info(f"时间序列频率设置为: {freq}, 样本数: {len(df)}")
        return df

    def _fill_and_generate_features(self, df: pd.DataFrame, window: int) -> pd.DataFrame:
        """
        根据时间序列填补缺失值并构造特征集合

        参数:
            df: 输入时间序列数据框
            window: 滚动窗口大小

        返回:
            包含生成特征的DataFrame
        """
        # 填充缺失值
        df['value'] = df['value'].interpolate('linear').bfill().ffill()

        # 检查是否有标签
        supervised = 'label' in df.columns
        if not supervised:
            df['label'] = 0  # 填充占位，方便处理无标签数据

        # 计算滚动窗口统计量
        rolling = df['value'].rolling(window, min_periods=1)
        df['rolling_mean'] = rolling.mean()
        df['rolling_std'] = rolling.std().fillna(1e-5)  # 避免除以0

        # 构造特征集合
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

        # 将特征转为DataFrame并合并
        features_df = pd.DataFrame(df_features, index=df.index)
        features_df['label'] = df['label']

        return features_df

    def generate_features(self, df: pd.DataFrame, freq: str = 'infer', window: int = 5) -> Tuple[pd.DataFrame, List[str]]:
        """
        生成特征并返回特征列表

        参数:
            df: 输入数据框
            freq: 时间序列频率，'infer'表示自动推断
            window: 滚动窗口大小

        返回:
            tuple: (特征数据框, 特征列名列表)
        """
        logger.info(f"开始生成特征，窗口大小: {window}, 频率: {freq}")

        # 确保时间戳列的处理统一
        if 'timestamp' not in df.columns:
            if df.index.name == 'timestamp':
                df = df.reset_index()
            else:
                raise ValueError("数据必须包含timestamp列或以timestamp为索引")

        # 设置频率并生成特征
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

    def visualize_anomaly_detection_results(self, test_df: pd.DataFrame,
                                            y_pred: np.ndarray,
                                            title: str = "异常检测结果",
                                            output_path: str = None) -> Dict[str, float]:
        """
        可视化异常检测结果并计算评估指标

        参数:
            test_df: 测试数据框
            y_pred: 预测的异常标签
            title: 图表标题
            output_path: 输出图表文件路径

        返回:
            包含评估指标的字典
        """
        if 'timestamp' in test_df.columns:
            test_df = test_df.set_index('timestamp')

        has_true_labels = 'label' in test_df.columns

        # 创建图表
        plt.figure(figsize=(15, 8))
        plt.plot(test_df.index, test_df['value'], label='原始数据')

        # 找出并绘制检测到的异常点
        anomaly_indices = np.where(y_pred == 1)[0]
        if len(anomaly_indices) > 0:
            anomaly_timestamps = test_df.index[anomaly_indices]
            anomaly_values = test_df['value'].iloc[anomaly_indices]
            plt.scatter(anomaly_timestamps, anomaly_values,
                        color='red', label='检测到的异常点', zorder=5)

        # 如果有真实标签，绘制真实异常点
        if has_true_labels:
            true_anomaly_indices = np.where(test_df['label'] == 1)[0]
            if len(true_anomaly_indices) > 0:
                true_anomaly_timestamps = test_df.index[true_anomaly_indices]
                true_anomaly_values = test_df['value'].iloc[true_anomaly_indices]
                plt.scatter(true_anomaly_timestamps, true_anomaly_values,
                            color='green', marker='x', s=100, label='真实异常点', zorder=4)

        # 设置图表属性
        plt.title(title)
        plt.xlabel('时间')
        plt.ylabel('数值')
        plt.legend()
        plt.grid(True)

        # 保存图表
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

            logger.info(f"评估指标: Accuracy={metrics['accuracy']:.4f}, "
                        f"Precision={metrics['precision']:.4f}, "
                        f"Recall={metrics['recall']:.4f}, "
                        f"F1={metrics['f1']:.4f}")

        return metrics

    def evaluate_model(self) -> Dict[str, float]:
        """
        评估模型性能，返回评估指标

        返回:
            包含模型评估指标的字典，如准确率、精确率、召回率、F1分数
        """
        if not hasattr(self, 'test_data') or self.test_data is None:
            logger.warning("没有测试数据，无法评估模型")
            return {}

        X_test, y_test = self.test_data
        if not hasattr(self, 'model') or self.model is None:
            logger.warning("模型未训练，无法评估")
            return {}

        # 预测
        try:
            y_pred = self.model.predict(X_test)

            # 转换算法特定的预测结果为标准格式 (1: 异常, 0: 正常)
            if hasattr(self, 'convert_predictions'):
                y_pred = self.convert_predictions(y_pred)

            # 计算评估指标
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

        except Exception as e:
            logger.error(f"模型评估失败: {str(e)}")
            return {'error': str(e)}

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        使用训练好的模型进行预测

        参数:
            data: DataFrame，包含待预测的时间序列数据

        返回:
            带有预测结果的DataFrame
        """
        # 验证前置条件
        if not hasattr(self, 'model') or self.model is None:
            raise ValueError("模型尚未训练或加载")

        if not hasattr(self, 'feature_columns') or not self.feature_columns:
            raise ValueError("特征列未定义")

        logger.info(f"开始预测，输入数据形状: {data.shape}")

        try:
            # 保存原始数据的副本
            original_data = data.copy()

            # 处理时间戳字段
            has_timestamp = 'timestamp' in data.columns

            # 从训练配置中获取窗口大小和频率
            window = self.train_config.get('window', 5)
            freq = self.train_config.get('freq', 'infer')

            # 预处理数据并生成特征
            if has_timestamp:
                processed_data, _ = self.generate_features(data, freq, window)
            else:
                processed_data, _ = self.generate_features(
                    data.reset_index().rename(
                        columns={data.index.name: 'timestamp'}),
                    freq, window
                )

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
                logger.debug("应用特征标准化")
                X = self.scaler.transform(X)

            # 预测
            y_pred = self.model.predict(X)

            # 转换预测结果为标准格式
            if hasattr(self, 'convert_predictions'):
                y_pred = self.convert_predictions(y_pred)

            # 创建包含预测结果的DataFrame
            prediction_df = pd.DataFrame(
                {'anomaly': y_pred}, index=processed_data.index)

            # 将预测结果合并回原始数据
            if has_timestamp:
                # 时间戳形式
                result = original_data.copy()
                result = result.set_index('timestamp')
                result = result.join(prediction_df[['anomaly']], how='left')
                result['anomaly'] = result['anomaly'].fillna(0).astype(int)
                result = result.reset_index()
            else:
                # 原索引形式
                result = original_data.copy()
                result = result.join(prediction_df[['anomaly']], how='left')
                result['anomaly'] = result['anomaly'].fillna(0).astype(int)

            # 统计异常点
            anomaly_count = result['anomaly'].sum()
            anomaly_ratio = anomaly_count / \
                len(result) if len(result) > 0 else 0
            logger.info(
                f"预测完成，检测到 {anomaly_count} 个异常点，占比 {anomaly_ratio:.2%}")

            return result

        except Exception as e:
            logger.error(f"预测过程发生错误: {str(e)}", exc_info=True)
            raise ValueError(f"预测失败: {str(e)}")

    def save_model(self, model_path: str) -> None:
        """
        保存模型到文件

        参数:
            model_path: 模型保存路径
        """
        # 确保父目录存在
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        # 保存状态
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns,
            'train_config': self.train_config,
            'scaler': self.scaler,
        }

        # 子类可以在_get_additional_model_data方法中添加额外需要保存的数据
        if hasattr(self, '_get_additional_model_data'):
            additional_data = self._get_additional_model_data()
            model_data.update(additional_data)

        joblib.dump(model_data, model_path)
        logger.info(f"模型已保存至: {model_path}")

    def load_model(self, model_path: str) -> None:
        """
        从文件加载模型

        参数:
            model_path: 模型文件路径
        """
        try:
            data = joblib.load(model_path)

            self.model = data['model']
            self.feature_columns = data['feature_columns']
            self.train_config = data['train_config']
            self.scaler = data.get('scaler')

            # 子类可以在_load_additional_model_data方法中处理额外的数据
            if hasattr(self, '_load_additional_model_data'):
                self._load_additional_model_data(data)

            logger.info(f"模型已从 {model_path} 加载")
            logger.debug(f"加载的特征列: {self.feature_columns}")

        except Exception as e:
            logger.error(f"加载模型失败: {str(e)}", exc_info=True)
            raise ValueError(f"无法加载模型: {str(e)}")

    @abc.abstractmethod
    def train(self, train_config: Dict[str, Any]) -> None:
        """
        训练异常检测模型

        参数:
            train_config: 训练配置字典

        实现此方法的子类应处理:
        1. 数据加载与预处理
        2. 特征生成
        3. 模型配置与训练
        4. 模型评估
        """
        pass

    def convert_predictions(self, y_pred: np.ndarray) -> np.ndarray:
        """
        将算法特定的预测结果转换为标准格式 (1: 异常, 0: 正常)

        子类可以重写此方法以处理特定算法的预测结果格式

        参数:
            y_pred: 原始预测结果

        返回:
            标准格式的预测结果
        """
        return y_pred

    def _process_training_data(self, train_config: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        处理训练数据，生成特征并准备模型输入

        参数:
            train_config: 训练配置字典

        返回:
            tuple: (特征矩阵X, 标签向量y, 特征列名列表)
        """
        logger.info("处理训练数据...")

        # 加载数据
        df = self.load_csv_data(train_config['train_data_path'])

        # 从配置获取参数
        freq = train_config.get('freq', 'infer')
        window = int(train_config.get('window', 5))

        # 生成特征
        df_features, feature_columns = self.generate_features(df, freq, window)
        logger.info(f"特征生成完成，共 {len(feature_columns)} 个特征")

        # 准备标签
        has_labels = 'label' in df_features.columns and df_features['label'].sum(
        ) > 0
        if has_labels:
            logger.info("检测到标签列，使用监督学习模式")
            y = df_features['label'].astype(int).values
        else:
            logger.info("无标签数据或标签全为0，使用无监督学习模式")
            y = np.zeros(len(df_features))

        # 准备特征矩阵
        X = df_features[feature_columns].values

        return X, y, feature_columns

    def _split_data(self, X: np.ndarray, y: np.ndarray, train_config: Dict[str, Any], supervised: bool = True) -> Tuple:
        """
        划分训练集、验证集和测试集

        参数:
            X: 特征矩阵
            y: 标签向量
            train_config: 训练配置
            supervised: 是否为监督学习

        返回:
            tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        test_size = train_config.get('test_size', 0.2)
        val_size = train_config.get('val_size', 0.1)
        random_state = train_config.get('random_state', 42)

        logger.info(f"划分数据集，测试集比例: {test_size}, 验证集比例: {val_size}")

        if supervised and np.sum(y > 0) > 0:
            # 监督学习且有异常标签，使用分层抽样
            X_train_val, X_test, y_train_val, y_test = train_test_split(
                X, y, test_size=test_size, stratify=y, random_state=random_state
            )
            X_train, X_val, y_train, y_val = train_test_split(
                X_train_val, y_train_val, test_size=val_size/(1-test_size),
                stratify=y_train_val, random_state=random_state
            )
        else:
            # 无监督学习或无异常标签，使用随机抽样
            X_train_val, X_test = train_test_split(
                X, test_size=test_size, random_state=random_state
            )
            X_train, X_val = train_test_split(
                X_train_val, test_size=val_size/(1-test_size), random_state=random_state
            )
            y_train = np.zeros(len(X_train)) if y is None else y[:len(X_train)]
            y_val = np.zeros(len(X_val)) if y is None else y[len(
                X_train):len(X_train)+len(X_val)]
            y_test = np.zeros(
                len(X_test)) if y is None else y[len(X_train)+len(X_val):]

        logger.info(
            f"数据集划分完成 - 训练集: {X_train.shape}, 验证集: {X_val.shape}, 测试集: {X_test.shape}")

        return X_train, X_val, X_test, y_train, y_val, y_test

    def _standardize_features(self, X_train: np.ndarray, X_val: np.ndarray = None, X_test: np.ndarray = None) -> Tuple:
        """
        标准化特征

        参数:
            X_train: 训练集特征
            X_val: 验证集特征
            X_test: 测试集特征

        返回:
            tuple: (标准化后的X_train, X_val, X_test)
        """
        logger.info("标准化特征...")
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)

        X_val_scaled = self.scaler.transform(
            X_val) if X_val is not None else None
        X_test_scaled = self.scaler.transform(
            X_test) if X_test is not None else None

        return X_train_scaled, X_val_scaled, X_test_scaled


# 工厂方法，根据算法名称创建适当的异常检测器
def create_detector(algorithm_name: str) -> BaseAnomalyDetection:
    """
    根据算法名称创建异常检测器实例

    参数:
        algorithm_name: 算法名称，支持 'xgbod', 'randomforest', 'iforest'

    返回:
        BaseAnomalyDetection 子类实例

    异常:
        ValueError: 如果算法名称不支持
    """
    algorithm_name = algorithm_name.lower()

    from src.anomaly_detection.xgbod_detector import XGBODDetector
    from src.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector
    from src.anomaly_detection.unsupervised_iforest_detector import UnsupervisedIForestDetector

    if algorithm_name == 'xgbod':
        return XGBODDetector()
    elif algorithm_name == 'randomforest':
        return RandomForestAnomalyDetector()
    elif algorithm_name == 'iforest':
        return UnsupervisedIForestDetector()
    else:
        raise ValueError(f"不支持的算法: {algorithm_name}")


# 工厂方法，从配置中加载模型
def load_model_from_config(model_id: str, algorithm: str, run_mode: str) -> BaseAnomalyDetection:
    """
    从配置中加载模型

    参数:
        model_id: 模型ID
        algorithm: 算法名称
        run_mode: 运行模式，'local'或'remote'

    返回:
        加载了模型的检测器实例

    异常:
        ValueError: 如果模型不存在或加载失败
    """
    detector = create_detector(algorithm)

    if run_mode.lower() == 'local':
        model_path = f"models/{algorithm.lower()}/{model_id}.pkl"
        if not os.path.exists(model_path):
            raise ValueError(f"本地模型文件不存在: {model_path}")

        detector.load_model(model_path)
        logger.info(f"从本地加载模型: {model_path}")

    else:
        raise ValueError("远程模型加载应由API处理")

    return detector
