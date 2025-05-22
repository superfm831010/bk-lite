"""
随机森林异常检测模块

实现基于随机森林的监督式异常检测算法，适用于有标签数据
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Tuple
import os
import joblib
import numpy as np
import pandas as pd
from sanic.log import logger

from src.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection


class RandomForestAnomalyDetector(BaseAnomalyDetection):
    """
    随机森林异常检测器

    使用随机森林分类器实现的监督式异常检测，需要带有标签的训练数据
    """

    def __init__(self):
        """初始化随机森林异常检测器"""
        super().__init__()

    def train(self, train_config: Dict[str, Any]):
        """
        训练随机森林异常检测模型

        参数:
            train_config: 训练配置字典，包含训练参数和数据路径
        """
        logger.info("开始训练随机森林异常检测模型")
        self.train_config = train_config

        try:
            # 1. 处理训练数据
            X, y, self.feature_columns = self._process_training_data(
                train_config)

            # 2. 检查标签
            if np.sum(y > 0) == 0:
                logger.warning("训练数据中没有异常样本标签，随机森林需要有标签数据")

            # 3. 数据集划分
            X_train, X_val, X_test, y_train, y_val, y_test = self._split_data(
                X, y, train_config, supervised=True
            )

            # 保存数据集引用
            self.train_data = (X_train, y_train)
            self.val_data = (X_val, y_val)
            self.test_data = (X_test, y_test)

            # 4. 特征标准化
            standardize = train_config.get('standardize', True)
            if standardize:
                X_train, X_val, X_test = self._standardize_features(
                    X_train, X_val, X_test)

            # 5. 配置模型
            hyper_params = train_config.get('hyper_params', {})
            model_params = {
                'n_estimators': hyper_params.get('n_estimators', 100),
                'max_depth': hyper_params.get('max_depth', 10),
                'min_samples_split': hyper_params.get('min_samples_split', 2),
                'min_samples_leaf': hyper_params.get('min_samples_leaf', 2),
                'max_features': hyper_params.get('max_features', 'sqrt'),
                'bootstrap': hyper_params.get('bootstrap', True),
                'random_state': train_config.get('random_state', 42),
                'class_weight': hyper_params.get('class_weight', 'balanced'),
                'n_jobs': hyper_params.get('n_jobs', -1)
            }

            logger.info(f"初始化随机森林模型，参数: {model_params}")
            self.model = RandomForestClassifier(**model_params)

            # 6. 训练模型
            logger.info("开始模型训练...")
            self.model.fit(X_train, y_train)

            # 7. 评估模型性能
            train_pred = self.model.predict(X_train)
            train_metrics = self._evaluate(y_train, train_pred)

            val_pred = self.model.predict(X_val)
            val_metrics = self._evaluate(y_val, val_pred)

            logger.info(
                f"模型训练完成，训练集 F1: {train_metrics['f1']:.4f}, 验证集 F1: {val_metrics['f1']:.4f}")

            # 8. 分析特征重要性
            self._analyze_feature_importance()

            return self

        except Exception as e:
            logger.error(f"随机森林模型训练失败: {str(e)}", exc_info=True)
            raise

    def _analyze_feature_importance(self):
        """分析并记录特征重要性"""
        if not hasattr(self, 'model') or not hasattr(self.model, 'feature_importances_'):
            logger.warning("模型不存在或没有特征重要性属性")
            return

        feature_importance = self.model.feature_importances_
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': feature_importance
        }).sort_values('importance', ascending=False)

        top_features = importance_df.head(10)

        logger.info("Top 10 特征重要性:")
        for i, (feature, importance) in enumerate(zip(top_features['feature'], top_features['importance'])):
            logger.info(f"  {i+1}. {feature}: {importance:.4f}")

    def evaluate_model(self) -> Dict[str, float]:
        """
        评估模型性能，使用测试集数据

        返回:
            包含评估指标的字典
        """
        if not hasattr(self, 'test_data') or self.test_data is None:
            logger.warning("没有测试数据，将使用验证集评估")
            X_test, y_test = self.val_data
        else:
            X_test, y_test = self.test_data

        if not hasattr(self, 'model') or self.model is None:
            logger.warning("模型尚未训练")
            return {'error': 'Model not trained'}

        try:
            y_pred = self.model.predict(X_test)
            metrics = self._evaluate(y_test, y_pred)

            logger.info(f"模型评估结果: Accuracy={metrics['accuracy']:.4f}, "
                        f"Precision={metrics['precision']:.4f}, "
                        f"Recall={metrics['recall']:.4f}, "
                        f"F1={metrics['f1']:.4f}")

            return metrics

        except Exception as e:
            logger.error(f"模型评估失败: {str(e)}")
            return {'error': str(e)}

    def _evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        计算评估指标

        参数:
            y_true: 真实标签
            y_pred: 预测标签

        返回:
            包含各项评估指标的字典
        """
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
        }

        # 计算异常检测特有的指标
        true_anomalies = np.sum(y_true == 1)
        if true_anomalies > 0:
            detected_anomalies = np.sum(y_pred == 1)
            metrics["anomaly_detection_rate"] = np.sum(
                (y_pred == 1) & (y_true == 1)) / true_anomalies
            metrics["false_alarm_rate"] = np.sum((y_pred == 1) & (
                y_true == 0)) / np.sum(y_true == 0) if np.sum(y_true == 0) > 0 else 0

        return metrics
