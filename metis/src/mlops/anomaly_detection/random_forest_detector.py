import uuid
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sanic.log import logger
from src import core
from src.mlops.mlops_utils import MLOpsUtils
from src.core.env.core_settings import core_settings
from mlflow.models import infer_signature
from hyperopt import hp, fmin, tpe, Trials, STATUS_OK
from typing import Dict, Any, Optional, Tuple

DEFAULT_HYPEROPT_SPACE = {
    "n_estimators": hp.randint("n_estimators", 100, 500),  # 增加树的数量范围
    "max_depth": hp.randint("max_depth", 10, 50),  # 增加树的深度范围
    "min_samples_split": hp.randint("min_samples_split", 2, 10),  # 降低分裂所需样本数
    "min_samples_leaf": hp.randint("min_samples_leaf", 1, 5),  # 降低叶子节点所需样本数
    # 增加特征选择范围
    "max_features": hp.choice("max_features", ["sqrt", "log2", None]),
    "bootstrap": hp.choice("bootstrap", [True, False]),  # 增加是否使用自助法选项
    # 增加权重选项
    "class_weight": hp.choice("class_weight", ["balanced", "balanced_subsample", None]),
}


class RandomForestAnomalyDetector:
    """随机森林异常检测器"""

    def predict(self, data: pd.DataFrame, model_name: str) -> pd.DataFrame:
        """使用训练好的模型进行异常检测预测"""
        mlflow.set_tracking_uri(core_settings.mlflow_tracking_uri)

        model_uri = f"models:/{model_name}/latest"
        model = mlflow.sklearn.load_model(model_uri)
        test_df, feature_columns = MLOpsUtils.prepare_timestamp_features(
            data, freq=model.freq, window=model.window
        )
        probabilities = model.predict_proba(test_df[feature_columns])[:, 1]
        return pd.DataFrame({
            'value': test_df['value'],
            'anomaly_probability': probabilities,
        })

    def _prepare_hyperopt_config(self, hyperopt_config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """准备超参数优化配置"""
        hyperopt_config = hyperopt_config or {}
        merged_space = {**DEFAULT_HYPEROPT_SPACE,
                        **hyperopt_config.get("space", {})}
        return {
            "space": merged_space,
            "max_evals": hyperopt_config.get("max_evals", 200),
            "algorithm": hyperopt_config.get("algorithm", tpe.suggest),
            "early_stop_patience": hyperopt_config.get("early_stop_patience", 20),
            "min_improvement": hyperopt_config.get("min_improvement", 0.00005)
        }

    def _load_and_prepare_data(self, path: str, freq: str, window: int) -> Tuple[pd.DataFrame, list]:
        """加载并准备数据"""
        df = MLOpsUtils.load_timestamp_csv_data(path)
        df, feature_columns = MLOpsUtils.prepare_timestamp_features(
            df, freq=freq, window=window)
        return df, feature_columns

    def train(
        self,
        experiment_name: str,
        train_data_path: str,
        val_data_path: str,
        test_data_path: str,
        freq: str = 'infer',
        window: int = 30,
        random_state: int = 42,
        hyperopt_config: Optional[Dict[str, Any]] = None,
        task_id: Optional[str] = str(uuid.uuid4())
    ) -> None:
        """
        训练随机森林模型并记录到MLflow
        """
        mlflow.set_tracking_uri(core_settings.mlflow_tracking_uri)
        print(f"当前MLflow跟踪URI: {core_settings.mlflow_tracking_uri}")
        mlflow.set_experiment(experiment_name)

        train_df, feature_columns = self._load_and_prepare_data(
            train_data_path, freq, window)
        X_train, y_train = train_df[feature_columns].values, train_df['label'].values
        logger.info(f"📁 训练集: {train_data_path}, 样本数: {len(X_train)}")

        val_df, _ = self._load_and_prepare_data(val_data_path, freq, window)
        X_val, y_val = val_df[feature_columns].values, val_df['label'].values
        logger.info(f"📁 验证集: {val_data_path}, 样本数: {len(X_val)}")

        test_df, _ = self._load_and_prepare_data(test_data_path, freq, window)
        X_test, y_test = test_df[feature_columns].values, test_df['label'].values
        logger.info(f"📁 测试集: {test_data_path}, 样本数: {len(X_test)}")

        config = self._prepare_hyperopt_config(hyperopt_config)
        logger.info(
            f"🚀 超参数优化: 最大评估{config['max_evals']}，早停耐心{config['early_stop_patience']}")

        trials = Trials()
        step_counter = 0
        best_loss = float('inf')
        no_improvement_count = 0

        def objective(params: Dict[str, Any]) -> Dict[str, Any]:
            nonlocal step_counter, best_loss, no_improvement_count
            step_counter += 1
            int_params = ['n_estimators', 'max_depth',
                          'min_samples_split', 'min_samples_leaf']
            converted_params = {
                k: int(v) if k in int_params and v is not None else v
                for k, v in params.items()
            }
            converted_params.update(
                {"random_state": random_state, "n_jobs": -1})
            model = RandomForestClassifier(**converted_params)
            model.fit(X_train, y_train)

            # 验证集评估
            y_val_pred = model.predict(X_val)
            val_metrics = MLOpsUtils.calculate_metrics(
                y_val, y_val_pred, subprefix='val')
            val_accuracy = (y_val == y_val_pred).mean()

            # 测试集评估（仅用于监控，不参与优化决策）
            y_test_pred = model.predict(X_test)
            test_metrics = MLOpsUtils.calculate_metrics(
                y_test, y_test_pred, subprefix='test')
            test_accuracy = (y_test == y_test_pred).mean()

            # 运维异常检测优化指标：优先保证召回率，平衡精确率
            recall = val_metrics.get('val_recall', 0.0)
            precision = val_metrics.get('val_precision', 0.0)
            f1 = val_metrics.get('val_f1', 0.0)

            # 使用加权组合指标：召回率权重更高，避免漏报
            weighted_score = 0.6 * recall + 0.3 * precision + 0.1 * f1
            current_loss = -weighted_score

            # 记录验证集指标（用于优化）
            mlflow.log_metric("val_f1", f1, step=step_counter)
            mlflow.log_metric("val_recall", recall, step=step_counter)
            mlflow.log_metric("val_precision", precision, step=step_counter)
            mlflow.log_metric("val_accuracy", val_accuracy, step=step_counter)

            # 记录测试集指标（仅监控，不用于优化决策）
            mlflow.log_metric("test_f1", test_metrics.get(
                'test_f1', 0.0), step=step_counter)
            mlflow.log_metric("test_recall", test_metrics.get(
                'test_recall', 0.0), step=step_counter)
            mlflow.log_metric("test_precision", test_metrics.get(
                'test_precision', 0.0), step=step_counter)
            mlflow.log_metric("test_accuracy", test_accuracy,
                              step=step_counter)

            if current_loss < best_loss - config['min_improvement']:
                best_loss = current_loss
                no_improvement_count = 0
                logger.info(f"✅ Step {step_counter}: Loss改善")
            else:
                no_improvement_count += 1
                logger.info(
                    f"⏳ Step {step_counter}: 无改进 ({no_improvement_count}/{config['early_stop_patience']})")

            logger.info(f"Step {step_counter}: Loss={current_loss:.6f}, " +
                        ", ".join([f"{k.capitalize()}={v:.4f}" for k, v in val_metrics.items()]))

            if no_improvement_count >= config['early_stop_patience']:
                logger.info(f"🛑 触发早停")
                return {"loss": current_loss, "status": "early_stop", "model": model, "val_f1": f1}

            return {"loss": current_loss, "status": STATUS_OK, "model": model, "val_f1": f1}

        with mlflow.start_run(run_name=task_id):

            try:
                fmin(
                    fn=objective,
                    space=config['space'],
                    algo=config['algorithm'],
                    max_evals=config['max_evals'],
                    trials=trials,
                    verbose=True
                )
            except Exception as e:
                if "early_stop" in str(e) or no_improvement_count >= config['early_stop_patience']:
                    logger.info("🎯 优化因早停而结束")
                else:
                    logger.error(f"❌ 优化过程出错: {e}")
                    raise

            if trials.trials:
                best_trial = min(
                    trials.trials, key=lambda x: x['result']['loss'])
                best_model = best_trial['result']['model']
                best_model.window = window
                best_model.freq = freq

                # 最终测试集评估
                y_test_pred_final = best_model.predict(X_test)
                final_test_metrics = MLOpsUtils.calculate_metrics(
                    y_test, y_test_pred_final, subprefix='final_test')
                val_f1 = best_trial['result']['val_f1']

                # 仅记录最重要的最终指标
                mlflow.log_metric("final_val_f1", val_f1)
                mlflow.log_metric(
                    "final_test_f1", final_test_metrics.get('final_test_f1', 0.0))
                mlflow.log_metric("final_test_recall",
                                  final_test_metrics.get('final_test_recall', 0.0))
                mlflow.log_metric("final_test_precision",
                                  final_test_metrics.get('final_test_precision', 0.0))

                # 记录最后使用的模型参数到mlflow
                final_params = best_model.get_params()
                mlflow.log_params(final_params)

                signature = infer_signature(
                    X_train, best_model.predict(X_train))
                mlflow.sklearn.log_model(
                    sk_model=best_model,
                    name="model",
                    registered_model_name=experiment_name,
                    input_example=X_train[:1].tolist(),
                    signature=signature
                )
                logger.info("🎉 超参数优化完成!")
                logger.info(
                    f"🏆 最佳验证F1: {val_f1:.4f} (Loss: {best_trial['result']['loss']:.6f})")
                logger.info(
                    f"📈 总试验次数: {len(trials.trials)}/{config['max_evals']}")
                logger.info(f"🎯 最终测试集性能已记录到MLflow")

            else:
                logger.error("❌ 没有成功的试验结果")
