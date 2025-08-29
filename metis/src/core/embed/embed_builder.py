from langchain_openai import OpenAIEmbeddings

from src.core.sanic_plus.utils.gpu_utils import GpuUtils


class EmbedBuilder:
    _embed_instances = {}

    @classmethod
    def get_local_embed_instance(cls, protocol: str):
        model_device = GpuUtils.choose_model_device()

        # local-gpu模式下，使用GPU
        if protocol.startswith('local-gpu:'):
            model_device = 'cuda'

        model_type = protocol.split(':')[1]
        model_name = protocol.split(':')[2]

        if model_type == 'huggingface_embedding':
            from langchain_huggingface import HuggingFaceEmbeddings

            cls._embed_instances[protocol] = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={'device': model_device},
                encode_kwargs={'normalize_embeddings': False},
                cache_folder="./models"
            )
            return cls._embed_instances[protocol]

        return None

    @staticmethod
    def get_embed(protocol: str, model_name: str = '', model_api_key: str = '', model_base_url: str = ''):
        if protocol.startswith('local:'):
            return EmbedBuilder.get_local_embed_instance(protocol)
        else:
            embeddings = OpenAIEmbeddings(
                model=model_name,
                api_key=model_api_key,
                base_url=model_base_url,
                timeout=300,  # 5分钟超时，适应批量嵌入操作
            )
            return embeddings
