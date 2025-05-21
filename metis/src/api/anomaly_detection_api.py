"""
异常检测API模块

提供异常检测的训练和预测接口，支持多种异常检测算法和数据处理方式。
可以处理本地和远程(Supabase)模型存储。
"""
import os
import tempfile
from typing import Dict, Any, Tuple

import pandas as pd
from sanic import Blueprint, json, HTTPResponse
from sanic.log import logger
from sanic_ext import validate

from src.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection, create_detector
from src.core.sanic_plus.auth.api_auth import auth
from src.entity.anomaly_detection.anomaly_detection_predict_request import AnomalyDetectionPredictRequest
from src.entity.anomaly_detection.anomaly_detection_train_request import AnomalyDetectionTrainRequest

anomaly_detection_api_router = Blueprint(
    "anomaly_detection", url_prefix="/anomaly_detection")

# 模型缓存字典，格式为 {f"{algorithm}:{model_id}": (detector_instance, model_path)}
MODEL_CACHE = {}


async def train_model_background(app, train_config):
    """
    在后台异步执行模型训练

    参数:
        app: Sanic应用实例
        train_config: 训练配置字典
    """
    temp_files = []  # 跟踪所有创建的临时文件

    try:
        # 1. 标准化训练配置
        train_config = _normalize_train_config(train_config)
        body = AnomalyDetectionTrainRequest(**train_config)

        logger.info(
            f"开始训练异常检测模型 [算法: {body.algorithm}, job_id: {body.job_id}]")

        # 2. 准备训练数据
        try:
            train_data_path, created_temp_file = _prepare_training_data(
                body.train_config)
            if created_temp_file:
                temp_files.append(train_data_path)
            body.train_config['train_data_path'] = train_data_path
        except Exception as e:
            logger.error(f"准备训练数据失败: {str(e)}")
            return

        # 3. 创建并训练检测器
        try:
            detector = create_detector(body.algorithm)
            logger.info(f"开始训练 {body.algorithm} 模型...")
            detector.train(body.train_config)
            logger.info(f"模型训练完成")
        except ValueError as e:
            logger.error(f"不支持的算法或训练失败: {str(e)}")
            return
        except Exception as e:
            logger.error(f"模型训练过程发生错误: {str(e)}", exc_info=True)
            return

        # 4. 评估模型(如果是监督学习)
        if body.supervised:
            try:
                evaluate_result = detector.evaluate_model()
                logger.info(f"模型评估结果: {evaluate_result}")
            except Exception as e:
                logger.warning(f"模型评估失败: {str(e)}, 但将继续保存模型")

        # 5. 保存模型
        try:
            if body.run_mode.lower() == "local":
                _save_model_locally(detector, body.algorithm, body.job_id)
            else:
                temp_model_path = _save_model_temporarily(detector)
                temp_files.append(temp_model_path)

                await _upload_model_to_supabase(app, temp_model_path, body.job_id)
        except Exception as e:
            logger.error(f"保存模型失败: {str(e)}", exc_info=True)

    except Exception as e:
        logger.error(f"模型训练过程失败: {str(e)}", exc_info=True)
    finally:
        # 清理所有临时文件
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                    logger.debug(f"已清理临时文件: {temp_file}")
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {str(e)}")


def _normalize_train_config(train_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    标准化训练配置，处理API兼容性问题

    参数:
        train_config: 原始训练配置

    返回:
        标准化后的训练配置
    """
    # 复制配置以避免修改原始对象
    config = train_config.copy()

    # 处理run_model和run_mode兼容性
    if 'run_model' in config and 'run_mode' not in config:
        config['run_mode'] = config.pop('run_model')
        logger.debug("已将参数'run_model'修正为'run_mode'")

    return config


def _prepare_training_data(train_config: Dict[str, Any]) -> Tuple[str, bool]:
    """
    准备训练数据，处理文件路径或内联数据

    参数:
        train_config: 训练配置

    返回:
        元组: (数据文件路径, 是否创建了临时文件)

    异常:
        ValueError: 如果无法准备训练数据
    """
    # 情况1: 已有训练数据路径
    if 'train_data_path' in train_config:
        data_path = train_config['train_data_path']
        if not os.path.exists(data_path):
            raise ValueError(f"训练数据文件不存在: {data_path}")

        logger.info(f"使用现有训练数据文件: {data_path}")
        return data_path, False

    # 情况2: 直接提供了训练数据
    train_data = train_config.get('train_data')
    if train_data and isinstance(train_data, list):
        # 创建临时CSV文件
        temp_csv = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)

        try:
            train_df = pd.DataFrame(train_data)
            train_df.to_csv(temp_csv.name, index=False)
            logger.info(f"已将{len(train_data)}条训练数据保存到临时文件: {temp_csv.name}")
            return temp_csv.name, True
        except Exception as e:
            # 出错时删除临时文件
            if os.path.exists(temp_csv.name):
                os.unlink(temp_csv.name)
            raise ValueError(f"处理训练数据失败: {str(e)}")

    # 两种情况都不满足
    raise ValueError("训练配置中既没有train_data_path也没有train_data，无法进行训练")


def _save_model_locally(detector: BaseAnomalyDetection, algorithm: str, job_id: str) -> str:
    """
    将模型保存到本地

    参数:
        detector: 训练好的检测器
        algorithm: 算法名称
        job_id: 模型ID

    返回:
        保存路径
    """
    save_dir = f"./models/{algorithm}"
    os.makedirs(save_dir, exist_ok=True)
    local_path = os.path.join(save_dir, f"{job_id}.pkl")
    detector.save_model(local_path)
    logger.info(f"模型已保存至本地: {local_path}")
    return local_path


def _save_model_temporarily(detector: BaseAnomalyDetection) -> str:
    """
    将模型保存到临时文件

    参数:
        detector: 训练好的检测器

    返回:
        临时文件路径
    """
    temp_file = tempfile.NamedTemporaryFile(suffix=".pkl", delete=False)
    model_path = temp_file.name
    detector.save_model(model_path)
    temp_file.close()
    return model_path


async def _upload_model_to_supabase(app, model_path: str, job_id: str) -> None:
    """
    将模型上传到Supabase

    参数:
        app: Sanic应用实例
        model_path: 模型文件路径
        job_id: 模型ID
    """
    if not hasattr(app.ctx, 'supabase'):
        raise ValueError("Supabase未配置，无法上传模型")

    with open(model_path, "rb") as f:
        data = f.read()

    supabase_path = f"models/{job_id}_model.pkl"
    await app.ctx.supabase.storage.from_("models").upload(
        path=supabase_path,
        file=data,
        file_options={
            "content-type": "application/octet-stream", "upsert": True}
    )

    logger.info(f"模型已上传至Supabase存储 [job_id: {job_id}]")


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
    """
    异常检测预测API

    接收时间序列数据，加载预训练模型进行异常检测预测
    """
    temp_files = []  # 临时文件跟踪

    try:
        # 1. 标准化请求参数
        model_id = body.model_id
        algorithm = body.algorithm.lower()
        run_mode = _get_run_mode(body)

        logger.info(
            f"开始异常检测预测，算法: {algorithm}, 模型ID: {model_id}, 运行模式: {run_mode}")

        # 2. 验证预测数据
        input_df = _validate_and_prepare_input_data(body.predict_data)

        # 3. 加载预训练模型
        try:
            detector, model_path = await _load_detector_model(
                request.app, algorithm, model_id, run_mode)

            # 添加临时文件以便清理（仅当模型是新下载的时候）
            # 注意：缓存使用的模型在API生命周期内不会被清理
            if run_mode == "remote" and os.path.exists(model_path) and not _is_model_cached(algorithm, model_id):
                temp_files.append(model_path)

        except FileNotFoundError as e:
            return json({"status": "error", "message": str(e)}, status=404)
        except ValueError as e:
            return json({"status": "error", "message": str(e)}, status=400)
        except Exception as e:
            logger.error(f"加载模型失败: {str(e)}", exc_info=True)
            return json({"status": "error", "message": f"加载模型失败: {str(e)}"}, status=500)

        # 4. 执行预测
        try:
            predict_result = detector.predict(input_df)

            # 5. 处理返回结果
            return _format_prediction_response(predict_result)

        except Exception as e:
            logger.error(f"预测过程失败: {str(e)}", exc_info=True)
            return json({"status": "error", "message": f"预测失败: {str(e)}"}, status=500)

    except Exception as e:
        logger.error(f"预测API调用失败: {str(e)}", exc_info=True)
        return json({"status": "error", "message": f"预测失败: {str(e)}"}, status=500)

    finally:
        # 清理所有临时文件（仅当不是缓存的模型时）
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass


def _get_run_mode(body: AnomalyDetectionPredictRequest) -> str:
    """获取规范化的运行模式"""
    # 兼容旧版API中的run_model参数
    if hasattr(body, 'run_model') and not hasattr(body, 'run_mode'):
        run_mode = getattr(body, 'run_model').lower()
        logger.debug("请求中检测到参数使用'run_model'，已自动修正为'run_mode'")
    else:
        run_mode = body.run_mode.lower()

    if run_mode not in ['local', 'remote']:
        raise ValueError("无效的run_mode参数，必须为'local'或'remote'")

    return run_mode


def _validate_and_prepare_input_data(predict_data) -> pd.DataFrame:
    """验证并准备输入数据"""
    if not predict_data or not isinstance(predict_data, list):
        raise ValueError("predict_data 不能为空且必须为数组")

    # 转换为DataFrame
    input_df = pd.DataFrame([dict(item) for item in predict_data])

    # 检查是否为空
    if input_df.empty:
        raise ValueError("predict_data 无有效记录")

    # 处理时间戳
    try:
        input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])
    except Exception as e:
        raise ValueError(f"时间戳格式无效: {str(e)}")

    # 确保必要字段存在
    required_fields = ['timestamp', 'value']
    missing_fields = [
        field for field in required_fields if field not in input_df.columns]
    if missing_fields:
        raise ValueError(f"输入数据缺少必要字段: {', '.join(missing_fields)}")

    logger.info(f"接收到 {len(input_df)} 条预测数据, 时间范围: "
                f"{input_df['timestamp'].min()} 到 {input_df['timestamp'].max()}")

    return input_df


def _is_model_cached(algorithm: str, model_id: str) -> bool:
    """
    检查模型是否已经在缓存中

    参数:
        algorithm: 算法名称
        model_id: 模型ID

    返回:
        布尔值: 模型是否在缓存中
    """
    cache_key = f"{algorithm}:{model_id}"
    return cache_key in MODEL_CACHE


async def _load_detector_model(app, algorithm: str, model_id: str, run_mode: str) -> Tuple[BaseAnomalyDetection, str]:
    """
    加载检测器模型，优先从内存缓存中加载

    参数:
        app: Sanic应用实例
        algorithm: 算法名称
        model_id: 模型ID
        run_mode: 运行模式 ('local'或'remote')

    返回:
        tuple: (检测器实例, 模型路径)
    """
    # 检查缓存中是否已有该模型
    cache_key = f"{algorithm}:{model_id}"
    if cache_key in MODEL_CACHE:
        logger.info(f"从内存缓存加载模型: {cache_key}")
        return MODEL_CACHE[cache_key]

    # 创建检测器
    detector = create_detector(algorithm)

    # 根据运行模式加载模型
    if run_mode == "local":
        model_path = f"models/{algorithm}/{model_id}.pkl"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"本地模型文件不存在: {model_path}")

        logger.info(f"从本地加载模型: {model_path}")

    elif run_mode == "remote":
        if not hasattr(app.ctx, "supabase"):
            raise ValueError("Supabase未配置，无法获取远程模型")

        supabase_path = f"models/{model_id}_model.pkl"
        try:
            model_data = app.ctx.supabase.storage.from_(
                "models").download(supabase_path)

            temp_file = tempfile.NamedTemporaryFile(
                suffix=".pkl", delete=False)
            model_path = temp_file.name
            temp_file.write(model_data)
            temp_file.close()

            logger.info(f"成功从Supabase获取模型: {model_id}")

        except Exception as e:
            raise FileNotFoundError(f"从Supabase获取模型失败: {str(e)}")

    else:
        raise ValueError("无效的run_mode参数，必须为'local'或'remote'")

    # 加载模型
    try:
        detector.load_model(model_path)
    except Exception as e:
        if os.path.exists(model_path) and run_mode == "remote":
            os.unlink(model_path)
        raise ValueError(f"模型文件格式错误或损坏: {str(e)}")

    # 将加载的模型保存到缓存
    MODEL_CACHE[cache_key] = (detector, model_path)
    logger.info(f"模型已加载并保存到内存缓存: {cache_key}")

    return detector, model_path


def _format_prediction_response(predict_result: pd.DataFrame) -> HTTPResponse:
    """
    格式化预测响应

    参数:
        predict_result: 预测结果DataFrame

    返回:
        HTTP响应
    """
    # 计算摘要信息
    anomaly_count = predict_result['anomaly'].sum()
    total_points = len(predict_result)
    anomaly_ratio = anomaly_count / total_points if total_points > 0 else 0

    logger.info(f"预测完成，检测到 {anomaly_count} 个异常点，占比 {anomaly_ratio:.2%}")

    # 转换时间戳为字符串
    predict_result['timestamp'] = predict_result['timestamp'].astype(str)

    # 构建响应
    return json({
        "status": "success",
        "summary": {
            "total_points": total_points,
            "anomaly_count": int(anomaly_count),
            "anomaly_ratio": float(anomaly_ratio)
        },
        "predictions": predict_result.to_dict(orient='records'),
    })
