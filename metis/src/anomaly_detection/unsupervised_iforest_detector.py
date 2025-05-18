from typing import Dict, Any
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import joblib
from sanic.log import logger
from src.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection


class UnsupervisedIForestDetector(BaseAnomalyDetection):
    def __init__(self):
        self._init_state()

    def _init_state(self):
        self.feature_columns = []
        self.train_config = {}
        self.model = None
        self.train_data = self.val_data = self.test_data = None
        self.scaler = None  # 添加特征标准化器

    def save_model(self, model_path: str):
        joblib.dump({
            'model': self.model,
            'feature_columns': self.feature_columns,
            'train_config': self.train_config,
            'scaler': self.scaler
        }, model_path)
        logger.info(f"模型已保存至: {model_path}")
        logger.info(f"保存的特征列: {self.feature_columns}")

    def load_model(self, model_path: str):
        data = joblib.load(model_path)
        self.model = data['model']
        self.feature_columns = data['feature_columns']
        self.train_config = data['train_config']
        self.scaler = data.get('scaler')  # 兼容旧模型
        logger.info(f"模型已从 {model_path} 加载")
        logger.info(f"加载的特征列: {self.feature_columns}")

    def convert_predictions(self, y_pred):
        """
        转换隔离森林预测结果 (-1: 异常, 1: 正常) 到标准格式 (1: 异常, 0: 正常)
        """
        return np.where(y_pred == -1, 1, 0)

    def train(self, train_config: Dict[str, Any]):
        """
        训练隔离森林无监督异常检测模型

        参数:
            train_config: 训练配置字典
        """
        logger.info(f"开始训练隔离森林异常检测模型, 配置: {train_config}")
        self.train_config = train_config

        # 加载数据
        df = self.load_csv_data(train_config['train_data_path'])

        # 从配置获取参数
        freq = train_config.get('freq', 'infer')
        window = int(train_config.get('window', 5))
        test_size = train_config.get('test_size', 0.2)
        random_state = train_config.get('random_state', 42)
        contamination = train_config.get('contamination', 0.05)  # 异常比例
        standardize = train_config.get('standardize', True)

        # 生成特征
        logger.info("开始生成特征...")
        df, self.feature_columns = self.generate_features(df, freq, window)

        logger.info(f"特征生成完成，特征列: {self.feature_columns}")

        # 准备训练数据
        X = df[self.feature_columns].values

        # 记录真实标签用于评估（如果有的话）
        has_labels = 'label' in df.columns and df['label'].sum() > 0
        if has_labels:
            y = df['label'].astype(int).values

        # 标准化特征
        if standardize:
            logger.info("应用特征标准化...")
            self.scaler = StandardScaler()
            X = self.scaler.fit_transform(X)

        # 数据划分
        if has_labels:
            logger.info(f"划分数据集，测试集比例: {test_size}")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            self.test_data = (X_test, y_test)
        else:
            logger.info("无标签数据，使用全部数据训练")
            X_train = X

        self.train_data = (X_train, None)

        # 配置模型
        hyper_params = train_config.get('hyper_params', {})
        hyper_params.setdefault('n_estimators', 100)
        hyper_params.setdefault('random_state', random_state)
        hyper_params.setdefault('contamination', contamination)

        logger.info(f"初始化隔离森林模型，参数: {hyper_params}")
        self.model = IsolationForest(**hyper_params)

        # 训练模型
        logger.info("开始模型训练...")
        self.model.fit(X_train)

        # 评估
        train_pred = self.convert_predictions(self.model.predict(X_train))
        anomaly_ratio = sum(train_pred) / len(train_pred)
        logger.info(f"模型训练完成，训练集发现异常比例: {anomaly_ratio:.2%}")

        if has_labels and hasattr(self, 'test_data'):
            test_pred = self.convert_predictions(self.model.predict(X_test))
            test_acc = accuracy_score(y_test, test_pred)
            test_prec = precision_score(y_test, test_pred, zero_division=0)
            test_recall = recall_score(y_test, test_pred, zero_division=0)
            test_f1 = f1_score(y_test, test_pred, zero_division=0)
            logger.info(f"测试集评估: 准确率={test_acc:.4f}, 精确率={test_prec:.4f}, "
                        f"召回率={test_recall:.4f}, F1={test_f1:.4f}")

        return self

    def evaluate_model(self) -> Dict[str, float]:
        if self.val_data is None:
            logger.warning("未设置验证集，跳过评估")
            return {}

        X_val, y_val = self.val_data
        y_pred = self.model.predict(X_val)
        y_pred = (y_pred == -1).astype(int)  # 转为二值标签: 1 表示异常

        if y_val is None:
            # 无监督场景：返回异常点比例
            anomaly_ratio = np.mean(y_pred)
            logger.info(f"验证集异常点比例: {anomaly_ratio:.4f}")
            return {
                "anomaly_ratio": anomaly_ratio
            }

        # 有监督场景：返回分类指标
        return self._evaluate(y_val, y_pred)

    def _evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
        }
