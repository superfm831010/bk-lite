import pandas as pd
from sanic import Blueprint, json
from sanic_ext import validate
import tempfile
import os
from src.core.sanic_plus.auth.api_auth import auth
from src.entity.anomaly_detection.anomaly_detection_predict_request import AnomalyDetectionPredictRequest
from src.entity.anomaly_detection.anomaly_detection_train_request import AnomalyDetectionTrainRequest
from sanic.log import logger
from src.anomaly_detection.xgbod_detector import XGBODDetector

anomaly_detection_api_router = Blueprint("anomaly_detection", url_prefix="/api/anomaly_detection")


async def train_model_background(app, train_config):
    body = AnomalyDetectionTrainRequest(**train_config)
    detector = None

    try:
        if body.algorithm == "xgbod":
            detector = XGBODDetector()
            detector.train(body.train_config)

        if body.supervised:
            evaluate_result = detector.evaluate_model()
            logger.info(f"模型评估结果: {evaluate_result}")

        if body.run_mode == "local":
            save_dir = f"./models/{body.algorithm}"
            os.makedirs(save_dir, exist_ok=True)
            local_path = os.path.join(save_dir, f"{body.job_id}.pkl")
            detector.save_model(local_path)
            logger.info(f"模型已保存至本地: {local_path}")
        else:
            # 上传至 Supabase
            with tempfile.NamedTemporaryFile(suffix=".pkl", delete=True) as tmp_file:
                model_path = tmp_file.name
                detector.save_model(model_path)

                with open(model_path, "rb") as f:
                    data = f.read()

                supabase_path = f"models/{body.job_id}_model.pkl"
                response = app.ctx.supabase.storage \
                    .from_("models") \
                    .upload(path=supabase_path, file=data,
                            file_options={"content-type": "application/octet-stream", "upsert": True})
                logger.info(f"模型已保存至 Supabase, job_id: {body.job_id}")
    except Exception as e:
        logger.error(f"模型训练失败: {e}", exc_info=True)


@anomaly_detection_api_router.post("/train")
@auth.login_required
@validate(json=AnomalyDetectionTrainRequest)
async def train(request, body: AnomalyDetectionTrainRequest):
    train_config = body.model_dump()
    job_id = body.job_id

    request.app.add_task(train_model_background(request.app, train_config))
    return json({"status": "success", "message": "模型训练已在后台启动", "job_id": job_id})


@anomaly_detection_api_router.post("/predict")
@auth.login_required
@validate(json=AnomalyDetectionPredictRequest)
async def predict(request, body: AnomalyDetectionPredictRequest):
    try:
        model_id = body.model_id
        run_mode = body.run_mode.lower()

        # 1. 加载模型
        if run_mode == "local":
            local_model_path = f"models/{body.algorithm}/{model_id}.pkl"
            if not os.path.exists(local_model_path):
                logger.error(f"本地模型文件不存在: {local_model_path}")
                return json({"status": "error", "message": f"模型文件不存在: {local_model_path}"}, status=404)

            model_path = local_model_path
            logger.info(f"从本地加载模型: {model_path}")

        elif run_mode == "remote":
            if not hasattr(request.app.ctx, "supabase"):
                logger.error("Supabase未配置，无法获取远程模型")
                return json({"status": "error", "message": "Supabase未配置"}, status=500)

            supabase_path = f"models/{model_id}_model.pkl"
            try:
                model_data = request.app.ctx.supabase.storage \
                    .from_("models") \
                    .download(supabase_path)

                temp_file = tempfile.NamedTemporaryFile(suffix=".pkl", delete=False)
                model_path = temp_file.name
                temp_file.write(model_data)
                temp_file.close()

                logger.info(f"成功从Supabase获取模型: {model_id}")
            except Exception as e:
                logger.error(f"从Supabase获取模型失败: {e}")
                return json({"status": "error", "message": f"获取模型失败: {str(e)}"}, status=404)

        else:
            return json({"status": "error", "message": "无效的run_mode参数，必须为'local'或'remote'"}, status=400)

        # 2. 使用用户提供的数据进行预测
        if not body.predict_data or not isinstance(body.predict_data, list):
            return json({"status": "error", "message": "predict_data 不能为空且必须为数组"}, status=400)

        input_df = pd.DataFrame(body.predict_data)

        if input_df.empty:
            return json({"status": "error", "message": "predict_data 无有效记录"}, status=400)

        logger.info(f"接收到 {len(input_df)} 条预测数据")

        # 3. 加载模型并预测
        detector = XGBODDetector()
        detector.load_model(model_path)

        predict_result = detector.predict(input_df)

        # 5. 返回结果
        return json({
            "status": "success",
            "predictions": predict_result.to_dict(orient='records'),
        })

    except Exception as e:
        logger.error(f"预测失败: {e}", exc_info=True)
        return json({"status": "error", "message": f"预测失败: {str(e)}"}, status=500)
