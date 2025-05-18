from pydantic import BaseModel


class AnomalyDetectionTrainRequest(BaseModel):
    algorithm: str = ''
    train_config: dict = {}
    supervised: bool = False
    job_id: str = ''
    run_mode: str = 'local'
