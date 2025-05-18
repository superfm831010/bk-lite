from typing import List

from pydantic import BaseModel


class AnomalyDetectionPredictRequest(BaseModel):
    model_id: str
    algorithm: str = ''
    run_mode: str = 'local'
    predict_data: List[dict]
