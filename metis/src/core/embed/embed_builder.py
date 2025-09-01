from typing import Optional, Dict, Any
from langchain_openai import OpenAIEmbeddings
from sanic.log import logger

from src.core.sanic_plus.utils.gpu_utils import GpuUtils


class EmbedBuilder:
    """嵌入模型构建器，支持本地和远程模型。"""

    _embed_instances: Dict[str, Any] = {}

    # 配置常量
    LOCAL_GPU_PREFIX = 'local-gpu:'
    LOCAL_PREFIX = 'local:'
    HUGGINGFACE_TYPE = 'huggingface_embedding'
    DEFAULT_TIMEOUT = 300  # 5分钟超时，适应批量嵌入操作
    DEFAULT_MODEL_CACHE = "./models"

    @classmethod
    def get_local_embed_instance(cls, protocol: str) -> Optional[Any]:
        """获取本地嵌入模型实例。

        Args:
            protocol: 协议字符串，格式为 'local:type:model_name' 或 'local-gpu:type:model_name'

        Returns:
            嵌入模型实例，如果不支持的类型则返回 None

        Raises:
            ValueError: 当协议格式不正确时
        """
        if not protocol or ':' not in protocol:
            logger.error(f"Invalid protocol format: {protocol}")
            raise ValueError(
                f"Protocol must contain ':' separator: {protocol}")

        try:
            parts = protocol.split(':')
            if len(parts) < 3:
                logger.error(
                    f"Protocol must have at least 3 parts: {protocol}")
                raise ValueError(
                    f"Protocol format should be 'prefix:type:model_name': {protocol}")

            model_type = parts[1]
            model_name = parts[2]

            # 检查是否已存在实例
            if protocol in cls._embed_instances:
                logger.debug(
                    f"Reusing existing embed instance for protocol: {protocol}")
                return cls._embed_instances[protocol]

            model_device = GpuUtils.choose_model_device()

            # local-gpu模式下，使用GPU
            if protocol.startswith(cls.LOCAL_GPU_PREFIX):
                model_device = 'cuda'
                logger.info(f"Using GPU device for protocol: {protocol}")
            else:
                logger.info(
                    f"Using device '{model_device}' for protocol: {protocol}")

            if model_type == cls.HUGGINGFACE_TYPE:
                from langchain_huggingface import HuggingFaceEmbeddings

                logger.info(
                    f"Creating HuggingFace embedding instance: {model_name}")
                cls._embed_instances[protocol] = HuggingFaceEmbeddings(
                    model_name=model_name,
                    model_kwargs={'device': model_device},
                    encode_kwargs={'normalize_embeddings': False},
                    cache_folder=cls.DEFAULT_MODEL_CACHE
                )
                return cls._embed_instances[protocol]
            else:
                logger.warning(f"Unsupported model type: {model_type}")
                return None

        except Exception as e:
            logger.error(
                f"Failed to create local embed instance for protocol '{protocol}': {e}")
            raise

    @staticmethod
    def get_embed(protocol: str, model_name: str = '', model_api_key: str = '', model_base_url: str = '') -> Any:
        """获取嵌入模型实例。

        Args:
            protocol: 协议字符串，本地模型使用 'local:' 或 'local-gpu:' 前缀
            model_name: 远程模型名称
            model_api_key: API密钥（敏感信息，不会被记录）
            model_base_url: API基础URL

        Returns:
            嵌入模型实例

        Raises:
            ValueError: 当参数校验失败时
        """
        if not protocol:
            raise ValueError("Protocol cannot be empty")

        try:
            if protocol.startswith(EmbedBuilder.LOCAL_PREFIX):
                logger.info(
                    f"Creating local embed instance with protocol: {protocol}")
                return EmbedBuilder.get_local_embed_instance(protocol)
            else:
                # 远程模型参数校验
                if not model_name:
                    raise ValueError(
                        "model_name is required for remote embedding")
                if not model_api_key:
                    raise ValueError(
                        "model_api_key is required for remote embedding")

                logger.info(
                    f"Creating OpenAI embedding instance with model: {model_name}")
                embeddings = OpenAIEmbeddings(
                    model=model_name,
                    api_key=model_api_key,
                    base_url=model_base_url,
                    timeout=EmbedBuilder.DEFAULT_TIMEOUT,
                )
                return embeddings

        except Exception as e:
            # 确保不输出敏感信息
            safe_protocol = protocol if not model_api_key else f"{protocol} (with API key)"
            logger.error(
                f"Failed to create embed instance for protocol '{safe_protocol}': {e}")
            raise
