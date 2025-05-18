from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any
import joblib
import numpy as np
import pandas as pd
from sanic.log import logger
from src.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection


class RandomForestAnomalyDetector(BaseAnomalyDetection):
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

    def train(self, train_config: Dict[str, Any]):
        """
        训练随机森林异常检测模型

        参数:
            train_config: 训练配置字典
        """
        logger.info(f"开始训练随机森林异常检测模型, 配置: {train_config}")
        self.train_config = train_config

        # 加载数据
        df = self.load_csv_data(train_config['train_data_path'])

        # 从配置获取参数
        freq = train_config.get('freq', 'infer')
        window = int(train_config.get('window', 5))
        test_size = train_config.get('test_size', 0.2)
        val_size = train_config.get('val_size', 0.1)
        random_state = train_config.get('random_state', 42)
        standardize = train_config.get('standardize', True)

        # 生成特征
        logger.info("开始生成特征...")
        df, self.feature_columns = self.generate_features(df, freq, window)

        logger.info(f"特征生成完成，特征列: {self.feature_columns}")

        # 准备训练数据
        X = df[self.feature_columns].values
        y = df['label'].astype(int).values

        # 标准化特征
        if standardize:
            logger.info("应用特征标准化...")
            self.scaler = StandardScaler()
            X = self.scaler.fit_transform(X)

        # 数据划分
        logger.info(f"划分数据集，测试集比例: {test_size}, 验证集比例: {val_size}")
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=random_state
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val, test_size=val_size/(1-test_size),
            stratify=y_train_val, random_state=random_state
        )

        self.train_data = (X_train, y_train)
        self.val_data = (X_val, y_val)
        self.test_data = (X_test, y_test)

        logger.info(
            f"训练集: {X_train.shape}, 验证集: {X_val.shape}, 测试集: {X_test.shape}")

        # 配置模型
        hyper_params = train_config.get('hyper_params', {})
        hyper_params.setdefault('n_estimators', 100)
        hyper_params.setdefault('max_depth', 10)
        hyper_params.setdefault('random_state', random_state)

        logger.info(f"初始化随机森林模型，参数: {hyper_params}")
        self.model = RandomForestClassifier(**hyper_params)

        # 训练模型
        logger.info("开始模型训练...")
        self.model.fit(X_train, y_train)

        # 评估训练集和验证集
        train_pred = self.model.predict(X_train)
        train_acc = accuracy_score(y_train, train_pred)

        val_pred = self.model.predict(X_val)
        val_acc = accuracy_score(y_val, val_pred)

        logger.info(f"模型训练完成，训练集准确率: {train_acc:.4f}, 验证集准确率: {val_acc:.4f}")

        # 特征重要性
        feature_importance = self.model.feature_importances_
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': feature_importance
        }).sort_values('importance', ascending=False)

        logger.info(f"前5个重要特征: {importance_df.head(5).to_dict('records')}")

        return self

    def evaluate_model(self) -> Dict[str, float]:
        X_val, y_val = self.val_data
        y_pred = self.model.predict(X_val)
        return self._evaluate(y_val, y_pred)

    def _evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
        }
