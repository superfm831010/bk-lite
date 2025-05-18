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
from src.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector
from src.anomaly_detection.unsupervised_iforest_detector import UnsupervisedIForestDetector

anomaly_detection_api_router = Blueprint(
    "anomaly_detection", url_prefix="/api/anomaly_detection")


async def train_model_background(app, train_config):
    try:
        # 修复run_model -> run_mode的问题
        if 'run_model' in train_config and 'run_mode' not in train_config:
            train_config['run_mode'] = train_config.pop('run_model')
            logger.info("检测到参数使用'run_model'，已自动修正为'run_mode'")

        body = AnomalyDetectionTrainRequest(**train_config)
        detector = None

        logger.info(f"开始训练模型，算法: {body.algorithm}, job_id: {body.job_id}")

        # 根据算法类型选择检测器
        if body.algorithm.lower() == "xgbod":
            detector = XGBODDetector()
        elif body.algorithm.lower() == "randomforest":
            detector = RandomForestAnomalyDetector()
        elif body.algorithm.lower() == "iforest":
            detector = UnsupervisedIForestDetector()
        else:
            logger.error(f"不支持的算法: {body.algorithm}")
            return

        # 处理训练数据
        # 检查train_config中是否包含train_data_path
        if 'train_data_path' in body.train_config:
            if not os.path.exists(body.train_config['train_data_path']):
                logger.error(
                    f"训练数据文件不存在: {body.train_config['train_data_path']}")
                return
            logger.info(
                f"将使用配置中指定的训练数据路径: {body.train_config['train_data_path']}")
        else:
            # 检查train_config中是否包含直接的训练数据
            train_data = body.train_config.get('train_data')
            if train_data and isinstance(train_data, list):
                temp_csv = tempfile.NamedTemporaryFile(
                    suffix='.csv', delete=False)
                try:
                    train_df = pd.DataFrame(train_data)
                    train_df.to_csv(temp_csv.name, index=False)
                    body.train_config['train_data_path'] = temp_csv.name
                    logger.info(
                        f"将{len(train_data)}条训练数据保存到临时文件: {temp_csv.name}")
                except Exception as e:
                    logger.error(f"保存训练数据到临时文件失败: {e}")
                    if os.path.exists(temp_csv.name):
                        os.unlink(temp_csv.name)
                    return
            else:
                logger.error("训练配置中既没有train_data_path也没有train_data，无法进行训练")
                return

        # 训练模型
        logger.info(f"开始使用{body.algorithm}训练异常检测模型...")
        detector.train(body.train_config)
        logger.info(f"模型训练完成")

        # 评估模型(如果是监督学习)
        if body.supervised:
            try:
                evaluate_result = detector.evaluate_model()
                logger.info(f"模型评估结果: {evaluate_result}")
            except Exception as e:
                logger.warning(f"模型评估失败: {e}, 但将继续保存模型")

        # 保存模型
        if body.run_mode.lower() == "local":
            save_dir = f"./models/{body.algorithm}"
            os.makedirs(save_dir, exist_ok=True)
            local_path = os.path.join(save_dir, f"{body.job_id}.pkl")
            detector.save_model(local_path)
            logger.info(f"模型已保存至本地: {local_path}")
        else:
            # 上传至 Supabase
            with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as tmp_file:
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

                # 清理临时文件
                os.unlink(model_path)

        # 清理训练数据临时文件
        if 'temp_csv' in locals() and os.path.exists(temp_csv.name):
            os.unlink(temp_csv.name)
            logger.info(f"清理临时训练数据文件")

    except Exception as e:
        logger.error(f"模型训练失败: {e}", exc_info=True)
        # 清理临时文件
        if 'temp_csv' in locals() and os.path.exists(temp_csv.name):
            os.unlink(temp_csv.name)


@anomaly_detection_api_router.post("/train")
@auth.login_required
@validate(json=AnomalyDetectionTrainRequest)
async def train(request, body: AnomalyDetectionTrainRequest):
    train_config = body.model_dump()
    job_id = body.job_id

    # 修复run_model -> run_mode的问题
    if 'run_model' in request.json and 'run_mode' not in request.json:
        train_config['run_mode'] = request.json.get('run_model')
        logger.info("API请求中检测到参数使用'run_model'，已自动修正为'run_mode'")

    request.app.add_task(train_model_background(request.app, train_config))
    return json({"status": "success", "message": "模型训练已在后台启动", "job_id": job_id})


@anomaly_detection_api_router.post("/predict")
@auth.login_required
@validate(json=AnomalyDetectionPredictRequest)
async def predict(request, body: AnomalyDetectionPredictRequest):
    try:
        model_id = body.model_id
        algorithm = body.algorithm.lower()
        run_mode = body.run_mode.lower()

        # 修复run_model -> run_mode的问题
        if hasattr(body, 'run_model') and not hasattr(body, 'run_mode'):
            run_mode = getattr(body, 'run_model').lower()
            logger.info("请求中检测到参数使用'run_model'，已自动修正为'run_mode'")

        logger.info(
            f"开始进行异常检测预测，算法: {algorithm}, 模型ID: {model_id}, 运行模式: {run_mode}")

        # 1. 加载模型
        if run_mode == "local":
            local_model_path = f"models/{algorithm}/{model_id}.pkl"
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

                temp_file = tempfile.NamedTemporaryFile(
                    suffix=".pkl", delete=False)
                model_path = temp_file.name
                temp_file.write(model_data)
                temp_file.close()

                logger.info(f"成功从Supabase获取模型: {model_id}")
            except Exception as e:
                logger.error(f"从Supabase获取模型失败: {e}")
                return json({"status": "error", "message": f"获取模型失败: {str(e)}"}, status=404)

        else:
            return json({"status": "error", "message": "无效的run_mode参数，必须为'local'或'remote'"}, status=400)

        # 2. 检查预测数据
        if not body.predict_data or not isinstance(body.predict_data, list):
            return json({"status": "error", "message": "predict_data 不能为空且必须为数组"}, status=400)

        input_df = pd.DataFrame([dict(item) for item in body.predict_data])
        input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])
        if input_df.empty:
            return json({"status": "error", "message": "predict_data 无有效记录"}, status=400)

        # 确保输入数据有必要的字段
        required_fields = ['timestamp', 'value']
        missing_fields = [
            field for field in required_fields if field not in input_df.columns]
        if missing_fields:
            return json({
                "status": "error",
                "message": f"输入数据缺少必要字段: {', '.join(missing_fields)}"
            }, status=400)

        logger.info(
            f"接收到 {len(input_df)} 条预测数据, 时间范围: {input_df['timestamp'].min()} 到 {input_df['timestamp'].max()}")

        # 3. 根据算法选择检测器并加载模型
        if algorithm == "xgbod":
            detector = XGBODDetector()
        elif algorithm == "randomforest":
            detector = RandomForestAnomalyDetector()
        elif algorithm == "iforest":
            detector = UnsupervisedIForestDetector()
        else:
            return json({"status": "error", "message": f"不支持的算法: {algorithm}"}, status=400)

        # 加载模型
        try:
            detector.load_model(model_path)
        except Exception as e:
            logger.error(f"加载模型失败: {e}", exc_info=True)
            return json({"status": "error", "message": f"加载模型失败: {str(e)}"}, status=500)

        # 清理远程模型的临时文件
        if run_mode == "remote" and os.path.exists(model_path):
            os.unlink(model_path)

        # 4. 预测
        try:

            predict_result = detector.predict(input_df)

            # 提取摘要信息
            anomaly_count = predict_result['anomaly'].sum()
            anomaly_ratio = anomaly_count / \
                len(predict_result) if len(predict_result) > 0 else 0

            logger.info(
                f"预测完成，检测到 {anomaly_count} 个异常点，占比 {anomaly_ratio:.2%}")

            # 5. 返回结果
            predict_result['timestamp'] = predict_result['timestamp'].astype(str)
            return json({
                "status": "success",
                "summary": {
                    "total_points": len(predict_result),
                    "anomaly_count": int(predict_result['anomaly'].sum()),
                    "anomaly_ratio": float(
                        predict_result['anomaly'].sum() / len(predict_result) if len(predict_result) > 0 else 0)
                },
                "predictions": predict_result.to_dict(orient='records'),
            })
        except Exception as e:
            logger.error(f"预测过程失败: {e}", exc_info=True)
            return json({"status": "error", "message": f"预测失败: {str(e)}"}, status=500)

    except Exception as e:
        logger.error(f"预测API调用失败: {e}", exc_info=True)
        return json({"status": "error", "message": f"预测失败: {str(e)}"}, status=500)
