"""
异常检测API单元测试
"""

import pytest
import json
import os
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock, Mock
import pandas as pd
from datetime import datetime, timedelta

from src.api.mlops.anomaly_detection_api import save_data_to_csv, train_model_background
from src.entity.mlops.anomaly_detection.anomaly_detection_train_request import TrainingDataPoint, AnomalyDetectionTrainRequest
from src.entity.mlops.anomaly_detection.anomaly_detection_predict_request import DataPoint, AnomalyDetectionPredictRequest


class TestAnomalyDetectionAPI:
    """异常检测API测试类"""

    @pytest.fixture
    def sample_train_data(self):
        """生成训练测试数据"""
        base_time = datetime.now()
        train_data = []
        val_data = []
        test_data = []

        # 生成20个训练样本
        for i in range(20):
            timestamp = (base_time + timedelta(hours=i)).isoformat()
            value = 1.0 + 0.1 * i + (0.5 if i % 10 == 0 else 0)  # 每10个点有一个异常
            label = 1 if i % 10 == 0 else 0
            train_data.append(TrainingDataPoint(
                timestamp=timestamp, value=value, label=label))

        # 生成10个验证样本
        for i in range(20, 30):
            timestamp = (base_time + timedelta(hours=i)).isoformat()
            value = 1.0 + 0.1 * i + (0.5 if i % 10 == 0 else 0)
            label = 1 if i % 10 == 0 else 0
            val_data.append(TrainingDataPoint(
                timestamp=timestamp, value=value, label=label))

        # 生成10个测试样本
        for i in range(30, 40):
            timestamp = (base_time + timedelta(hours=i)).isoformat()
            value = 1.0 + 0.1 * i + (0.5 if i % 10 == 0 else 0)
            label = 1 if i % 10 == 0 else 0
            test_data.append(TrainingDataPoint(
                timestamp=timestamp, value=value, label=label))

        return AnomalyDetectionTrainRequest(
            experiment_name="test_experiment",
            train_data=train_data,
            val_data=val_data,
            test_data=test_data,
            freq="1H",
            window=10
        )

    @pytest.fixture
    def sample_predict_data(self):
        """生成预测测试数据"""
        base_time = datetime.now()
        data = []

        for i in range(10):
            timestamp = (base_time + timedelta(hours=i)).isoformat()
            value = 1.0 + 0.1 * i
            data.append(DataPoint(timestamp=timestamp, value=value))

        return AnomalyDetectionPredictRequest(
            model_name="test_experiment",
            model_version="latest",
            data=data
        )

    @pytest.mark.asyncio
    async def test_train_model_background_success(self, sample_train_data):
        """测试后台训练任务成功执行"""
        task_id = "test_task_123"
        mock_app = Mock()

        with patch('src.mlops.anomaly_detection.random_forest_detector.RandomForestAnomalyDetector') as mock_detector_class:
            # 模拟检测器
            mock_detector = MagicMock()
            mock_detector_class.return_value = mock_detector
            mock_detector.train = MagicMock()

            # 执行后台训练任务
            await train_model_background(mock_app, task_id, sample_train_data)

            # 验证train方法被调用
            mock_detector.train.assert_called_once()
            call_args = mock_detector.train.call_args[0]

            # 验证调用参数
            assert call_args[0] == "test_experiment"  # experiment_name
            assert call_args[4] == "1H"  # freq
            assert call_args[5] == 10  # window
            assert call_args[6] == 42  # random_state
