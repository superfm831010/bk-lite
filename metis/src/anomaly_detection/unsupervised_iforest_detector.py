"""
无监督隔离森林异常检测模块

实现基于隔离森林(Isolation Forest)的无监督异常检测算法，
可以在无标签数据上进行训练和异常检测
"""
from typing import Dict, Any, List, Tuple, Optional
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import joblib
import os
from sanic.log import logger

from src.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection


class UnsupervisedIForestDetector(BaseAnomalyDetection):
    """
    无监督隔离森林异常检测器

    使用隔离森林算法进行无监督异常检测，适用于未标记数据
    隔离森林的核心思想是通过随机选择特征和阈值来构建树，
    异常点通常更易于被"隔离"，因此可以通过树高来识别
    """

    def __init__(self):
        """初始化无监督隔离森林检测器"""
        super().__init__()

    def convert_predictions(self, y_pred: np.ndarray) -> np.ndarray:
        """
        转换隔离森林预测结果 (-1: 异常, 1: 正常) 到标准格式 (1: 异常, 0: 正常)

        参数:
            y_pred: 原始预测结果，其中-1表示异常，1表示正常

        返回:
            转换后的预测结果，其中1表示异常，0表示正常
        """
        return np.where(y_pred == -1, 1, 0)

    def train(self, train_config: Dict[str, Any]):
        """
        训练隔离森林无监督异常检测模型

        参数:
            train_config: 训练配置字典，包含训练参数和数据路径
        """
        logger.info("开始训练隔离森林无监督异常检测模型")
        self.train_config = train_config

        try:
            # 1. 处理训练数据
            X, y, self.feature_columns = self._process_training_data(
                train_config)

            # 2. 记录是否有标签用于评估
            has_labels = np.any(y > 0) if y is not None else False
            if has_labels:
                logger.info("检测到标签数据，将用于模型评估")
            else:
                logger.info("无标签数据，将使用无监督学习模式")

            # 3. 数据集划分
            test_size = train_config.get('test_size', 0.2)
            random_state = train_config.get('random_state', 42)

            if has_labels:
                # 有标签时进行分层划分
                X_train, X_test, y_train, y_test = self._split_data(
                    X, y, train_config, supervised=True)
                self.test_data = (X_test, y_test)
            else:
                # 无标签时随机划分
                if test_size > 0:
                    train_indices = np.random.RandomState(random_state).choice(
                        np.arange(len(X)),
                        size=int(len(X)*(1-test_size)),
                        replace=False
                    )
                    test_indices = np.array(
                        [i for i in range(len(X)) if i not in train_indices])

                    X_train = X[train_indices]
                    X_test = X[test_indices]
                    logger.info(
                        f"数据集划分完成 - 训练集: {X_train.shape}, 测试集: {X_test.shape}")
                else:
                    X_train = X
                    X_test = None
                    logger.info(f"使用全部数据训练，数据形状: {X_train.shape}")

            self.train_data = (X_train, None if not has_labels else y_train)

            # 4. 特征标准化
            standardize = train_config.get('standardize', True)
            if standardize:
                X_train, X_test = self._standardize_features(X_train, X_test)[
                    :2]

            # 5. 配置模型参数
            contamination = train_config.get('contamination', 0.05)
            hyper_params = train_config.get('hyper_params', {})

            model_params = {
                'n_estimators': hyper_params.get('n_estimators', 100),
                'max_samples': hyper_params.get('max_samples', 'auto'),
                'max_features': hyper_params.get('max_features', 1.0),
                'bootstrap': hyper_params.get('bootstrap', False),
                'n_jobs': hyper_params.get('n_jobs', -1),
                'random_state': random_state,
                'contamination': contamination,
                'verbose': 0
            }

            logger.info(f"初始化隔离森林模型，参数: {model_params}")
            self.model = IsolationForest(**model_params)

            # 6. 训练模型
            logger.info("开始训练模型...")
            self.model.fit(X_train)

            # 7. 评估训练结果
            self._evaluate_training_results(
                X_train, X_test, y_test if has_labels else None)

            logger.info("隔离森林模型训练完成")
            return self

        except Exception as e:
            logger.error(f"隔离森林模型训练失败: {str(e)}", exc_info=True)
            raise

    def _evaluate_training_results(self, X_train, X_test=None, y_test=None):
        """
        评估模型训练结果

        参数:
            X_train: 训练特征
            X_test: 测试特征
            y_test: 测试标签(如果有)
        """
        # 评估训练集异常比例
        train_pred_raw = self.model.predict(X_train)
        train_pred = self.convert_predictions(train_pred_raw)
        anomaly_ratio = np.mean(train_pred)
        logger.info(f"训练集异常比例: {anomaly_ratio:.2%}")

        # 决策函数分布统计
        train_scores = self.model.decision_function(X_train)
        logger.info(f"训练集决策函数统计 - 平均值: {np.mean(train_scores):.4f}, "
                    f"中位数: {np.median(train_scores):.4f}, "
                    f"最小值: {np.min(train_scores):.4f}, "
                    f"最大值: {np.max(train_scores):.4f}")

        # 如果有测试集和标签，计算评估指标
        if X_test is not None and y_test is not None:
            test_pred_raw = self.model.predict(X_test)
            test_pred = self.convert_predictions(test_pred_raw)

            metrics = {
                "accuracy": accuracy_score(y_test, test_pred),
                "precision": precision_score(y_test, test_pred, zero_division=0),
                "recall": recall_score(y_test, test_pred, zero_division=0),
                "f1": f1_score(y_test, test_pred, zero_division=0),
            }

            logger.info(f"测试集评估: Accuracy={metrics['accuracy']:.4f}, "
                        f"Precision={metrics['precision']:.4f}, "
                        f"Recall={metrics['recall']:.4f}, "
                        f"F1={metrics['f1']:.4f}")

        # 如果有测试集但无标签，只计算异常比例
        elif X_test is not None:
            test_pred_raw = self.model.predict(X_test)
            test_pred = self.convert_predictions(test_pred_raw)
            test_anomaly_ratio = np.mean(test_pred)
            logger.info(f"测试集异常比例: {test_anomaly_ratio:.2%}")

    def evaluate_model(self) -> Dict[str, float]:
        """
        评估模型性能

        返回:
            包含评估指标的字典
        """
        if not hasattr(self, 'model') or self.model is None:
            logger.warning("模型尚未训练")
            return {'error': 'Model not trained'}

        # 优先使用测试数据
        if hasattr(self, 'test_data') and self.test_data is not None:
            X_test, y_test = self.test_data
            data_name = "测试集"
        elif hasattr(self, 'val_data') and self.val_data is not None:
            X_test, y_test = self.val_data
            data_name = "验证集"
        else:
            logger.warning("没有测试数据或验证数据，将使用训练数据评估")
            if hasattr(self, 'train_data') and self.train_data is not None:
                X_test, y_test = self.train_data
                data_name = "训练集"
            else:
                logger.error("没有可用数据进行评估")
                return {'error': 'No data available for evaluation'}

        try:
            # 获取原始预测结果和转换后的预测结果
            raw_pred = self.model.predict(X_test)
            y_pred = self.convert_predictions(raw_pred)

            # 计算决策函数值
            decision_scores = self.model.decision_function(X_test)

            # 基本统计指标
            metrics = {
                'anomaly_ratio': float(np.mean(y_pred)),
                'decision_score_mean': float(np.mean(decision_scores)),
                'decision_score_std': float(np.std(decision_scores)),
                'decision_score_min': float(np.min(decision_scores)),
                'decision_score_max': float(np.max(decision_scores)),
            }

            logger.info(f"{data_name}异常比例: {metrics['anomaly_ratio']:.2%}")
            logger.info(f"{data_name}决策函数统计: "
                        f"均值={metrics['decision_score_mean']:.4f}, "
                        f"标准差={metrics['decision_score_std']:.4f}")

            # 如果有真实标签，计算有监督评估指标
            if y_test is not None and np.sum(y_test) > 0:
                supervised_metrics = self._evaluate(y_test, y_pred)
                metrics.update(supervised_metrics)

                logger.info(f"{data_name}评估(有标签): "
                            f"Accuracy={metrics['accuracy']:.4f}, "
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
        predicted_anomalies = np.sum(y_pred == 1)

        if true_anomalies > 0:
            # 检测率 (Detection Rate)
            metrics["detection_rate"] = np.sum(
                (y_pred == 1) & (y_true == 1)) / true_anomalies

        if np.sum(y_true == 0) > 0:
            # 虚警率 (False Alarm Rate)
            metrics["false_alarm_rate"] = np.sum(
                (y_pred == 1) & (y_true == 0)) / np.sum(y_true == 0)

        return metrics
