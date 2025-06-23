import logging
import os

import numpy as np
import pandas as pd

from src.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector
from src.anomaly_detection.unsupervised_iforest_detector import UnsupervisedIForestDetector
from src.anomaly_detection.xgbod_detector import XGBODDetector
from src.core.aiops.aiops_utils import AiopsUtils
from tests.anomaly_detection.utils import (
    generate_training_data,
    generate_test_data_with_indices,
)

logger = logging.getLogger(__name__)


def test_unsupervised_iforest_detector_train():
    detector = UnsupervisedIForestDetector()
    detector_workflow(detector, job_name="unsupervised_iforest", train_config={
        "freq": "infer",
        "window": 30,
        "hyper_params": {}
    }, supervised=False)


def test_random_forest_train():
    detector = RandomForestAnomalyDetector()
    detector.train(
        experiment_name="random_forest",
        train_data_path='./tests/assert/anomaly_detection_train_randomforest.csv',
        window=30,
        freq='infer'
    )


def test_random_forest_detector_predict():
    detector = RandomForestAnomalyDetector()
    df = AiopsUtils.load_timestamp_csv_data(
        './tests/assert/anomaly_detection_test_randomforest.csv')
    results_df = detector.predict(df, 'random_forest')
    print(results_df)


def test_xgbod_detector_train():
    detector = XGBODDetector()
    detector_workflow(detector, job_name="xgbod", train_config={
        "freq": "infer",
        "window": 30,
        "hyper_params": {}
    }, supervised=True)


def detector_workflow(detector, job_name: str, train_config: dict,
                      supervised):
    os.makedirs("./test_results", exist_ok=True)
    train_df = generate_training_data(supervised=supervised)
    train_path = f"./test_results/anomaly_detection_train_{job_name}.csv"
    train_df.to_csv(train_path, index=False)

    logger.info("🔧 开始训练模型...")
    detector.train(
        run_name=job_name,
        train_data_path=train_path,
        **train_config
    )
    logger.info("✅ 模型训练完成")
