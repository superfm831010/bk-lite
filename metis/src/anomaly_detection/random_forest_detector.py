"""
随机森林异常检测模块

实现基于随机森林的监督式异常检测算法，适用于有标签数据
"""

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sanic.log import logger
from src.core.aiops.aiops_utils import AiopsUtils
from src.core.env.core_settings import core_settings
from mlflow.models import infer_signature

DEFAULT_HYPER_PARAMS = {
    "n_estimators": 300,
    "max_depth": None,
    "min_samples_split": 5,
    "min_samples_leaf": 3,
    "max_features": "sqrt",
    "bootstrap": True,
    "random_state": 42,
    "class_weight": "balanced_subsample",
    "n_jobs": -1
}


class RandomForestAnomalyDetector():
    def predict(self, data: pd.DataFrame, model_name):
        model_uri = f"models:/{model_name}/latest"
        model = mlflow.sklearn.load_model(model_uri)

        test_df, feature_columns = AiopsUtils.prepare_timestamp_features(
            data, freq=model.freq, window=model.window
        )

        # 只传入特征列进行预测
        test_features = test_df[feature_columns]
        probabilities = model.predict_proba(test_features)[:, 1]
        results_df = pd.DataFrame({
            'value': test_df['value'],
            'anomaly_probability': probabilities,
        })
        return results_df

    def train(self,
              experiment_name: str,
              train_data_path: str,
              freq: str = 'infer',
              window: int = 30,
              test_size: float = 0.2,
              val_size: float = 0.1,
              random_state: int = 42) -> None:
        """
        训练随机森林模型并记录到 MLflow
        """
        mlflow.set_tracking_uri(core_settings.mlflow_tracking_uri)
        mlflow.set_experiment(experiment_name)
        mlflow.autolog()
        with mlflow.start_run() as run:
            # 加载并处理数据
            df = AiopsUtils.load_timestamp_csv_data(train_data_path)
            df, feature_columns = AiopsUtils.prepare_timestamp_features(
                df, freq=freq, window=window)
            X = df[feature_columns].values

            y = df['label'].values

            X_train, X_val, X_test, y_train, y_val, y_test = AiopsUtils.split_timestamp_train_data(
                X, y, test_size=test_size, val_size=val_size, random_state=random_state
            )

            # 模型初始化与训练
            model_params = {**DEFAULT_HYPER_PARAMS}

            model = RandomForestClassifier(**model_params)
            model.fit(X_train, y_train)

            # 批量评估所有数据集
            datasets = [
                ("train", X_train, y_train),
                ("val", X_val, y_val),
                ("test", X_test, y_test)
            ]

            for dataset_name, X_data, y_true in datasets:
                y_pred = model.predict(X_data)
                metrics = AiopsUtils.calculate_metrics(
                    y_true, y_pred, dataset_name)
                mlflow.log_metrics(metrics)

            # 记录特征重要性
            AiopsUtils.log_importance_features(model, feature_columns)

            model.window = window
            model.freq = freq

            signature = infer_signature(X_train, model.predict(X_train))
            # 记录模型
            mlflow.sklearn.log_model(
                sk_model=model,
                name="model",
                registered_model_name=experiment_name,
                input_example=X_train[:1].tolist(),
                signature=signature
            )
