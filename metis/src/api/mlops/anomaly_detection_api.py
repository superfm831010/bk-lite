import os
import pandas as pd
import tempfile
import uuid
from sanic import Blueprint, json
from sanic_ext import validate
from sanic.log import logger

from src.core.sanic_plus.auth.api_auth import auth
from src.entity.mlops.anomaly_detection.anomaly_detection_predict_request import AnomalyDetectionPredictRequest
from src.entity.mlops.anomaly_detection.anomaly_detection_train_request import AnomalyDetectionTrainRequest
from src.entity.mlops.anomaly_detection.anomaly_detection_train_response import AnomalyDetectionTrainResponse
from src.entity.mlops.anomaly_detection.anomaly_detection_predict_response import AnomalyDetectionPredictResponse
from src.mlops.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector

anomaly_detection_api_router = Blueprint(
    "anomaly_detection", url_prefix="/anomaly_detection")


def save_data_to_csv(data_points, temp_dir: str, filename: str) -> str:
    """将数据点保存为CSV文件"""
    df = pd.DataFrame([point.dict() for point in data_points])
    file_path = os.path.join(temp_dir, filename)
    df.to_csv(file_path, index=False)
    return file_path


def load_detector(algorithm: str):
    """根据算法名称加载相应的检测器"""
    if algorithm == "RandomForest":
        return RandomForestAnomalyDetector()
    else:
        raise ValueError(f"不支持的算法: {algorithm}")


async def train_model_background(app, task_id: str, request: AnomalyDetectionTrainRequest):
    """Sanic后台训练任务"""
    try:
        logger.info(f"开始训练任务 {task_id}")

        # 创建临时目录保存数据
        with tempfile.TemporaryDirectory() as temp_dir:
            # 保存数据为CSV文件
            train_path = save_data_to_csv(
                request.train_data, temp_dir, "train.csv")
            val_path = save_data_to_csv(
                request.val_data, temp_dir, "val.csv")
            test_path = save_data_to_csv(
                request.test_data, temp_dir, "test.csv")

            # 创建检测器并训练
            logger.info(f"使用算法 {request.algorithm} 训练模型")
            detector = load_detector(request.algorithm)
            detector.train(
                request.experiment_name,
                train_path,
                val_path,
                test_path,
                freq=request.freq,
                window=request.window,
                random_state=request.random_state,
                hyperopt_config=request.hyperopt_config
            )

        logger.info(f"训练任务 {task_id} 完成")

    except Exception as e:
        logger.error(f"训练任务 {task_id} 失败: {e}")


@anomaly_detection_api_router.post("/train")
@auth.login_required
@validate(json=AnomalyDetectionTrainRequest)
async def train(request, body: AnomalyDetectionTrainRequest):
    """训练异常检测模型"""
    try:
        # 生成任务ID
        task_id = str(uuid.uuid4())

        # 启动Sanic后台任务
        request.app.add_task(train_model_background(
            request.app, task_id, body))

        # 返回任务信息
        response = AnomalyDetectionTrainResponse(
            task_id=task_id,
            experiment_name=body.experiment_name,
            status="started",
            message="训练任务已启动"
        )

        return json(response.model_dump())

    except Exception as e:
        logger.error(f"启动训练任务失败: {e}")
        return json({"error": f"启动训练任务失败: {str(e)}"}, status=500)


@anomaly_detection_api_router.post("/predict")
@auth.login_required
@validate(json=AnomalyDetectionPredictRequest)
async def predict(_, body: AnomalyDetectionPredictRequest):
    """异常检测预测"""
    try:
        # 准备输入数据
        input_df = pd.DataFrame([point.model_dump() for point in body.data])
        input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])
        input_df = input_df.reset_index(drop=True)

        # 创建检测器并预测
        detector = load_detector(body.algorithm)

        # 使用模型版本构建模型名称
        result_df = detector.predict(
            input_df, model_name=body.model_name, model_version=body.model_version)

        # 重置结果DataFrame的索引
        result_df = result_df.reset_index(drop=True)

        # 构建响应
        predictions = []
        anomaly_count = 0

        for idx, row in result_df.iterrows():
            is_anomaly = row['anomaly_probability'] > body.anomaly_threshold
            if is_anomaly:
                anomaly_count += 1

            predictions.append({
                "timestamp": input_df.iloc[idx]['timestamp'].isoformat(),
                "value": float(row['value']),
                "anomaly_probability": float(row['anomaly_probability']),
                "is_anomaly": is_anomaly
            })

        response = AnomalyDetectionPredictResponse(
            model_name=body.model_name,
            model_version=body.model_version if body.model_version != "latest" else "1",
            predictions=predictions,
            total_points=len(predictions),
            anomaly_count=anomaly_count,
            anomaly_rate=anomaly_count /
            len(predictions) if predictions else 0.0
        )

        return json(response.model_dump())

    except Exception as e:
        logger.error(f"异常检测预测失败: {e}")
        return json({"error": f"预测失败: {str(e)}"}, status=500)
