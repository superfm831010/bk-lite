import os
from loguru import logger

from src.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector
from src.anomaly_detection.xgbod_detector import XGBODDetector
from tests.anomaly_detection.utils import (
    generate_training_data,
    generate_test_data_with_indices,
)
from src.anomaly_detection.unsupervised_iforest_detector import UnsupervisedIForestDetector


def test_unsupervised_iforest_detector_train():
    detector = UnsupervisedIForestDetector()
    detector_workflow(detector, job_name="unsupervised_iforest", train_config={
        "freq": "infer",
        "window": 30,
        "hyper_params": {}
    }, supervised=False)


def test_random_forest_detector():
    rf_detector = RandomForestAnomalyDetector()
    detector_workflow(rf_detector, job_name="randomforest", train_config={
        "freq": "infer",
        "window": 30,
        "hyper_params": {
            'n_estimators': 100,
            'max_depth': 5,
            'random_state': 42
        }
    }, supervised=True)


def test_xgbod_detector_train():
    detector = XGBODDetector()
    detector_workflow(detector, job_name="xgbod", train_config={
        "freq": "infer",
        "window": 30,
        "hyper_params": {}
    }, supervised=True)


def detector_workflow(detector, job_name: str, train_config: dict,
                      supervised):
    """
    完整测试一个异常检测器的生命周期：
    - 数据生成
    - 模型训练
    - 模型评估
    - 模型保存/加载
    - 外部预测
    - 可视化与评估
    """
    os.makedirs("./test_results", exist_ok=True)

    # Step 1: 生成训练数据
    train_df = generate_training_data(supervised=supervised)
    train_path = f"./test_results/anomaly_detection_train_{job_name}.csv"
    train_df.to_csv(train_path, index=False)
    train_config['train_data_path'] = train_path

    logger.info("🔧 开始训练模型...")
    detector.train(train_config)
    logger.info("✅ 模型训练完成")

    # Step 2: 模型评估
    if supervised is True:
        logger.info("📊 开始评估模型...")
        evaluate_result = detector.evaluate_model()
        logger.info("🔍 评估结果: "
                    f"Accuracy: {evaluate_result['accuracy']:.4f}, "
                    f"Precision: {evaluate_result['precision']:.4f}, "
                    f"Recall: {evaluate_result['recall']:.4f}, "
                    f"F1: {evaluate_result['f1']:.4f}")

    # Step 3: 模型保存
    model_path = f"./test_results/{job_name}_model.pkl"
    detector.save_model(model_path)

    # Step 4: 生成测试数据
    test_df, anomaly_indices = generate_test_data_with_indices()
    test_path = f"./test_results/anomaly_detection_test_{job_name}.csv"
    test_df.to_csv(test_path, index=False)

    # Step 5: 加载模型并预测
    logger.info("📦 加载模型进行预测...")
    detector.load_model(model_path)
    predict_result = detector.predict(test_df)

    # Step 6: 可视化与性能评估
    logger.info("🖼️ 开始可视化并评估外部预测结果...")
    metrics = detector.visualize_anomaly_detection_results(
        test_df=test_df,
        y_pred=predict_result["anomaly"].values,
        title=f"{job_name.upper()} 外部预测 - 异常检测结果",
        output_path=f"./test_results/anomaly_detection_test_results_{job_name}.png",
    )

    logger.info("📈 外部预测评估结果: "
                f"Precision: {metrics['precision']:.4f}, "
                f"Recall: {metrics['recall']:.4f}, "
                f"F1: {metrics['f1']:.4f}")

    # Step 7: 简单断言确保模型有效
    assert metrics["f1"] > 0.1, "F1 分数过低，可能模型无效"
