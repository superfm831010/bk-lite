import logging

from src.mlops.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector
from src.mlops.mlops_utils import MLOpsUtils


logger = logging.getLogger(__name__)


def test_train():
    detector = RandomForestAnomalyDetector()
    detector.train(
        experiment_name="dev_random_forest",
        train_data_path='./tests/assert/anomaly_detection_train_randomforest.csv',
        val_data_path='./tests/assert/anomaly_detection_test_randomforest.csv',
        test_data_path='./tests/assert/anomaly_detection_test_randomforest.csv',
        window=30,
        freq='infer'
    )


def test_random_forest_detector_predict():
    detector = RandomForestAnomalyDetector()
    df = MLOpsUtils().load_timestamp_csv_data(
        './tests/assert/anomaly_detection_test_randomforest.csv'
    )
    results_df = detector.predict(df, 'dev_random_forest')
    print(results_df)
