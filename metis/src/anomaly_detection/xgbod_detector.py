from typing import Dict, Any, List, Tuple
import os
import joblib
import numpy as np
import pandas as pd
from sanic.log import logger
from pyod.models.xgbod import XGBOD
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection


class XGBODDetector(BaseAnomalyDetection):
    def __init__(self):
        self._init_state()

    def _init_state(self):
        self.feature_columns = []
        self.train_config = {}
        self.model = None
        self.train_data = self.val_data = self.test_data = None
        self.scaler = None  # 特征标准化器
        self.base_estimators = []  # 基础模型列表

    def save_model(self, model_path: str):
        # 确保父目录存在
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        joblib.dump({
            'model': self.model,
            'feature_columns': self.feature_columns,
            'train_config': self.train_config,
            'scaler': self.scaler,
            'base_estimators': self.base_estimators
        }, model_path)
        logger.info(f"模型已保存至: {model_path}")
        logger.info(f"保存的特征列: {self.feature_columns}")

    def load_model(self, model_path: str):
        data = joblib.load(model_path)
        self.model = data['model']
        self.feature_columns = data['feature_columns']
        self.train_config = data['train_config']
        self.scaler = data.get('scaler')
        self.base_estimators = data.get('base_estimators', [])
        logger.info(f"模型已从 {model_path} 加载")
        logger.info(f"加载的特征列: {self.feature_columns}")
        if self.base_estimators:
            logger.info(f"加载了{len(self.base_estimators)}个基础检测器")

    def train(self, train_config: Dict[str, Any]):
        """
        训练 XGBOD 模型用于异常检测

        参数:
            train_config: 训练配置字典，包含以下键:
                - train_data_path: 训练数据CSV文件路径
                - freq: 时间序列频率，默认为'infer'
                - window: 滚动窗口大小，默认为5
                - test_size: 测试集比例，默认为0.2
                - val_size: 验证集比例，默认为0.1
                - random_state: 随机种子，默认为42
                - hyper_params: XGBOD模型参数字典
                - standardize: 是否标准化特征，默认为True
                - contamination: 异常比例，默认为0.05
        """
        logger.info(f"开始训练XGBOD异常检测模型，配置: {train_config}")
        self.train_config = train_config

        # 1. 加载数据并进行预处理
        df = self.load_csv_data(train_config['train_data_path'])

        # 2. 获取配置参数
        freq = train_config.get('freq', 'infer')
        window = int(train_config.get('window', 5))
        test_size = train_config.get('test_size', 0.2)
        val_size = train_config.get('val_size', 0.1)
        random_state = train_config.get('random_state', 42)
        standardize = train_config.get('standardize', True)
        contamination = train_config.get('contamination', 0.05)

        # 3. 生成特征
        logger.info("开始生成特征...")
        df, self.feature_columns = self.generate_features(df, freq, window)
        logger.info(f"特征生成完成，特征数量: {len(self.feature_columns)}")

        # 4. 处理监督/无监督情况
        supervised = 'label' in df.columns and df['label'].sum() > 0
        if supervised:
            logger.info("检测到标签列，使用监督学习模式")
            y = df['label'].astype(int).values
        else:
            logger.info("无标签数据或标签全为0，使用无监督学习模式")
            y = np.zeros(len(df))

        # 5. 准备特征数据
        X = df[self.feature_columns].values

        # 6. 特征标准化
        if standardize:
            logger.info("应用特征标准化...")
            self.scaler = StandardScaler()
            X = self.scaler.fit_transform(X)

        # 7. 数据集划分
        logger.info(f"划分数据集，测试集比例: {test_size}, 验证集比例: {val_size}")
        if supervised:
            X_train_val, X_test, y_train_val, y_test = train_test_split(
                X, y, test_size=test_size, stratify=y, random_state=random_state
            )
            X_train, X_val, y_train, y_val = train_test_split(
                X_train_val, y_train_val, test_size=val_size/(1-test_size),
                stratify=y_train_val, random_state=random_state
            )
        else:
            X_train_val, X_test = train_test_split(
                X, test_size=test_size, random_state=random_state
            )
            X_train, X_val = train_test_split(
                X_train_val, test_size=val_size/(1-test_size), random_state=random_state
            )
            y_train = np.zeros(len(X_train))
            y_val = np.zeros(len(X_val))
            y_test = np.zeros(len(X_test))

        self.train_data = (X_train, y_train)
        self.val_data = (X_val, y_val)
        self.test_data = (X_test, y_test)

        logger.info(
            f"训练集: {X_train.shape}, 验证集: {X_val.shape}, 测试集: {X_test.shape}")

        # 8. 初始化并配置模型
        hyper_params = train_config.get('hyper_params', {})

        # 设置基础检测器
        self.base_estimators = []
        for i in range(hyper_params.get('n_base_estimators', 3)):
            name = f"IForest_{i}"
            estimator = IForest(contamination=contamination,
                                random_state=random_state+i)
            self.base_estimators.append((name, estimator))

        self.base_estimators.append(('LOF', LOF(contamination=contamination)))

        # 配置XGBOD
        xgb_params = {
            'max_depth': hyper_params.get('max_depth', 5),
            'n_estimators': hyper_params.get('n_estimators', 100),
            'learning_rate': hyper_params.get('learning_rate', 0.1),
            'random_state': random_state,
            'contamination': contamination,
        }

        logger.info(
            f"初始化XGBOD模型，参数: {xgb_params}, 基础检测器: {len(self.base_estimators)}个")
        self.model = XGBOD(
            base_estimators=self.base_estimators,
            **xgb_params
        )

        # 9. 训练模型
        logger.info(f"开始训练XGBOD模型...")
        self.model.fit(X_train, y_train if supervised else None)

        # 10. 评估模型
        # XGBOD的预测结果是0/1，其中1表示异常，不需要转换
        train_scores = self.model.decision_scores_
        train_pred = self.model.labels_

        anomaly_ratio = sum(train_pred) / len(train_pred)
        logger.info(f"模型训练完成，训练集发现异常比例: {anomaly_ratio:.2%}")

        if supervised:
            train_acc = accuracy_score(y_train, train_pred)
            train_prec = precision_score(y_train, train_pred, zero_division=0)
            train_recall = recall_score(y_train, train_pred, zero_division=0)
            train_f1 = f1_score(y_train, train_pred, zero_division=0)

            logger.info(f"训练集评估: 准确率={train_acc:.4f}, 精确率={train_prec:.4f}, "
                        f"召回率={train_recall:.4f}, F1={train_f1:.4f}")

            # 验证集评估
            val_pred = self.model.predict(X_val)
            val_acc = accuracy_score(y_val, val_pred)
            val_prec = precision_score(y_val, val_pred, zero_division=0)
            val_recall = recall_score(y_val, val_pred, zero_division=0)
            val_f1 = f1_score(y_val, val_pred, zero_division=0)

            logger.info(f"验证集评估: 准确率={val_acc:.4f}, 精确率={val_prec:.4f}, "
                        f"召回率={val_recall:.4f}, F1={val_f1:.4f}")

        return self
