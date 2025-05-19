"""
XGBOD异常检测模块

实现基于XGBOD (XGBoost Outlier Detection) 的异常检测器，
结合多种基础检测器和梯度提升树方法进行高精度异常检测
"""
from typing import Dict, Any, List, Tuple, Optional
import os
import numpy as np
import pandas as pd
from sanic.log import logger
from pyod.models.xgbod import XGBOD
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection


class XGBODDetector(BaseAnomalyDetection):
    """
    XGBOD异常检测器

    结合多个基础检测器的预测结果，通过XGBoost进行集成学习
    """

    def __init__(self):
        """初始化XGBOD检测器"""
        super().__init__()
        self.base_estimators = []  # 基础模型列表

    def _get_additional_model_data(self) -> Dict[str, Any]:
        """
        获取需要额外保存的模型数据

        返回:
            包含额外模型数据的字典
        """
        return {'base_estimators': self.base_estimators}

    def _load_additional_model_data(self, data: Dict[str, Any]) -> None:
        """
        加载额外的模型数据

        参数:
            data: 包含模型数据的字典
        """
        self.base_estimators = data.get('base_estimators', [])

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
        logger.info(f"开始训练XGBOD异常检测模型")
        self.train_config = train_config

        try:
            # 1. 处理训练数据
            X, y, self.feature_columns = self._process_training_data(
                train_config)

            # 2. 提取配置参数
            standardize = train_config.get('standardize', True)
            random_state = train_config.get('random_state', 42)
            contamination = train_config.get('contamination', 0.05)

            # 3. 数据集划分
            # 修复: 不再尝试使用'in'操作符检查布尔值
            # 如果supervised是布尔值，直接使用；如果是字典，检查'label'是否在其中
            supervised_value = train_config.get('supervised', True)
            is_supervised = supervised_value if isinstance(
                supervised_value, bool) else 'label' in supervised_value

            X_train, X_val, X_test, y_train, y_val, y_test = self._split_data(
                X, y, train_config, supervised=is_supervised
            )

            # 保存数据集引用
            self.train_data = (X_train, y_train)
            self.val_data = (X_val, y_val)
            self.test_data = (X_test, y_test)

            # 4. 特征标准化
            if standardize:
                X_train, X_val, X_test = self._standardize_features(
                    X_train, X_val, X_test)

            # 5. 设置基础检测器
            self._setup_base_estimators(train_config)

            # 6. 配置XGBOD模型
            self._configure_model(train_config)

            # 7. 训练模型
            logger.info("开始训练XGBOD模型...")
            self.model.fit(X_train, y_train if np.any(y_train > 0) else None)

            # 8. 评估模型
            self._evaluate_training_results(X_train, X_val, y_train, y_val)

            logger.info("XGBOD模型训练完成")
            return self

        except Exception as e:
            logger.error(f"XGBOD模型训练失败: {str(e)}", exc_info=True)
            raise

    def _setup_base_estimators(self, train_config: Dict[str, Any]) -> None:
        """
        设置XGBOD的基础检测器

        参数:
            train_config: 训练配置
        """
        hyper_params = train_config.get('hyper_params', {})
        random_state = train_config.get('random_state', 42)
        contamination = train_config.get('contamination', 0.05)
        n_estimators = hyper_params.get('n_base_estimators', 3)

        # 添加隔离森林检测器
        self.base_estimators = []
        for i in range(n_estimators):
            name = f"IForest_{i}"
            estimator = IForest(
                contamination=contamination,
                random_state=random_state+i,
                n_estimators=hyper_params.get('iforest_estimators', 100)
            )
            self.base_estimators.append((name, estimator))

        # 添加LOF检测器
        self.base_estimators.append((
            'LOF',
            LOF(contamination=contamination,
                n_neighbors=hyper_params.get('lof_neighbors', 20))
        ))

        logger.info(f"设置了 {len(self.base_estimators)} 个基础检测器")

    def _configure_model(self, train_config: Dict[str, Any]) -> None:
        """
        配置XGBOD模型参数

        参数:
            train_config: 训练配置
        """
        hyper_params = train_config.get('hyper_params', {})
        random_state = train_config.get('random_state', 42)
        contamination = train_config.get('contamination', 0.05)

        # 配置XGBoost参数
        xgb_params = {
            'max_depth': hyper_params.get('max_depth', 5),
            'n_estimators': hyper_params.get('n_estimators', 100),
            'learning_rate': hyper_params.get('learning_rate', 0.1),
            'random_state': random_state,
            'contamination': contamination,
        }

        logger.info(f"配置XGBOD模型，参数: {xgb_params}")
        self.model = XGBOD(
            base_estimators=self.base_estimators,
            **xgb_params
        )

    def _evaluate_training_results(self, X_train, X_val, y_train, y_val):
        """
        评估模型训练结果

        参数:
            X_train: 训练特征
            X_val: 验证特征
            y_train: 训练标签
            y_val: 验证标签
        """
        # 获取训练集预测结果
        train_pred = self.model.labels_
        anomaly_ratio = sum(train_pred) / \
            len(train_pred) if len(train_pred) > 0 else 0
        logger.info(f"训练集发现异常比例: {anomaly_ratio:.2%}")

        supervised = np.sum(y_train > 0) > 0

        # 监督学习模式下计算评估指标
        if supervised:
            train_metrics = {
                'accuracy': accuracy_score(y_train, train_pred),
                'precision': precision_score(y_train, train_pred, zero_division=0),
                'recall': recall_score(y_train, train_pred, zero_division=0),
                'f1': f1_score(y_train, train_pred, zero_division=0)
            }

            logger.info(f"训练集评估: Accuracy={train_metrics['accuracy']:.4f}, "
                        f"Precision={train_metrics['precision']:.4f}, "
                        f"Recall={train_metrics['recall']:.4f}, "
                        f"F1={train_metrics['f1']:.4f}")

            # 验证集评估
            if X_val is not None and len(X_val) > 0:
                val_pred = self.model.predict(X_val)
                val_metrics = {
                    'accuracy': accuracy_score(y_val, val_pred),
                    'precision': precision_score(y_val, val_pred, zero_division=0),
                    'recall': recall_score(y_val, val_pred, zero_division=0),
                    'f1': f1_score(y_val, val_pred, zero_division=0)
                }

                logger.info(f"验证集评估: Accuracy={val_metrics['accuracy']:.4f}, "
                            f"Precision={val_metrics['precision']:.4f}, "
                            f"Recall={val_metrics['recall']:.4f}, "
                            f"F1={val_metrics['f1']:.4f}")
