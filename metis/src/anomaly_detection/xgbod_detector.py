from typing import Dict, Any
import joblib
import numpy as np
import pandas as pd
from loguru import logger
from pyod.models.xgbod import XGBOD
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

from src.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection


class XGBODDetector(BaseAnomalyDetection):
    def __init__(self):
        self._init_state()

    def _init_state(self):
        self.feature_columns = []
        self.train_config = {}
        self.model = None
        self.train_data = self.val_data = self.test_data = None

    def save_model(self, model_path: str):
        joblib.dump({
            'model': self.model,
            'feature_columns': self.feature_columns,
            'train_config': self.train_config
        }, model_path)
        logger.info(f"模型已保存至: {model_path}")

    def load_model(self, model_path: str):
        data = joblib.load(model_path)
        self.model = data['model']
        self.feature_columns = data['feature_columns']
        self.train_config = data['train_config']
        logger.info(f"模型已从 {model_path} 加载")

    def train(self, train_config: Dict[str, Any]):
        self.train_config = train_config
        df = self.load_csv_data(train_config['train_data_path'])

        freq = train_config.get('freq', 'infer')
        window = int(train_config.get('window', 5))
        df, self.feature_columns = self.generate_features(df, freq, window)

        test_size = train_config.get('test_size', 0.2)
        val_size = train_config.get('val_size', 0.1)
        random_state = train_config.get('random_state', 42)

        X = df[self.feature_columns].values
        y = df['label'].astype(int).values

        # 数据划分
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=random_state
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val, test_size=val_size, stratify=y_train_val, random_state=random_state
        )

        self.train_data = (X_train, y_train)
        self.val_data = (X_val, y_val)
        self.test_data = (X_test, y_test)

        logger.info(f"训练集大小: {len(X_train)}, 验证集: {len(X_val)}, 测试集: {len(X_test)}")
        logger.debug(
            f"异常比例 - Train: {np.mean(y_train):.4f}, Val: {np.mean(y_val):.4f}, Test: {np.mean(y_test):.4f}")

        # 训练模型
        model_params = train_config.get('hyper_params', {})
        logger.info(f"开始训练 XGBOD 模型, 参数: {model_params}")
        self.model = XGBOD(base_estimators=[], **model_params)
        self.model.fit(X_train, y_train)
        logger.info("XGBOD 模型训练完成")

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

    def predict(self, input_df: pd.DataFrame) -> pd.DataFrame:
        logger.info(f"开始预测，共 {len(input_df)} 条数据")

        if not {'timestamp', 'value'}.issubset(input_df.columns):
            raise ValueError("输入数据必须包含 'timestamp' 和 'value' 字段")

        predict_df = input_df.copy()
        predict_df['label'] = predict_df.get('label', 0)

        freq = self.train_config.get('freq', 'infer')
        window = int(self.train_config.get('window', 5))
        processed_df, _ = self.generate_features(predict_df, freq, window)

        for col in self.feature_columns:
            if col not in processed_df:
                processed_df[col] = 0  # 填补缺失特征

        X = processed_df[self.feature_columns].values
        y_pred = self.model.predict(X)

        result_df = input_df.copy()
        result_df['anomaly'] = y_pred
        logger.info(f"预测完成，检测到异常点数量: {np.sum(y_pred)}")

        return result_df
