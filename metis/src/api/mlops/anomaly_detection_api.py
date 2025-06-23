"""
异常检测API模块

提供异常检测的训练和预测接口，支持多种异常检测算法和数据处理方式。
可以处理本地和远程(Supabase)模型存储。
"""

from sanic import Blueprint
from sanic_ext import validate

from src.core.sanic_plus.auth.api_auth import auth
from src.entity.anomaly_detection.anomaly_detection_predict_request import AnomalyDetectionPredictRequest
from src.entity.anomaly_detection.anomaly_detection_train_request import AnomalyDetectionTrainRequest

anomaly_detection_api_router = Blueprint(
    "anomaly_detection", url_prefix="/anomaly_detection")


async def train_model_background(app, train_config):
    pass


@anomaly_detection_api_router.post("/train")
@auth.login_required
@validate(json=AnomalyDetectionTrainRequest)
async def train(request, body: AnomalyDetectionTrainRequest):
    pass


@anomaly_detection_api_router.post("/predict")
@auth.login_required
@validate(json=AnomalyDetectionPredictRequest)
async def predict(request, body: AnomalyDetectionPredictRequest):
    pass
