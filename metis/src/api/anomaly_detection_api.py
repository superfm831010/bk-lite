from sanic import Blueprint
from sanic_ext import validate

from src.core.web.api_auth import auth
from src.entity.anomaly_detection.anomaly_detection_predict_request import AnomalyDetectionPredictRequest
from src.entity.anomaly_detection.anomaly_detection_train_request import AnomalyDetectionTrainRequest

rag_api_router = Blueprint("anomaly_detection", url_prefix="/anomaly_detection")


@rag_api_router.post("/train")
@auth.login_required
@validate(json=AnomalyDetectionTrainRequest)
async def train(request, body: AnomalyDetectionTrainRequest):
    pass


@rag_api_router.post("/predict")
@auth.login_required
@validate(json=AnomalyDetectionPredictRequest)
async def predict(request, body: AnomalyDetectionPredictRequest):
    pass
