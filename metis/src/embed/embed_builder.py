from langchain_openai import OpenAIEmbeddings
from sanic.log import logger


class EmbedBuilder:
    _embed_instances = {}

    @classmethod
    def get_embed_instance(cls, protocol: str):
        model_type = protocol.split(':')[1]
        model_name = protocol.split(':')[2]
        if model_type == 'huggingface_embedding' and cls._embed_instances.get(protocol, None) is None:
            from langchain_huggingface import HuggingFaceEmbeddings

            cls._embed_instances[protocol] = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': False},
                cache_folder="./models"
            )
        return cls._embed_instances[protocol]

    @staticmethod
    def get_embed(protocol: str, model_name: str = '', model_api_key: str = '', model_base_url: str = ''):
        if protocol.startswith('local:'):
            logger.info(f"加载本地Embed模型: {protocol}")
            return EmbedBuilder.get_embed_instance(protocol)
        else:
            logger.info(f"加载远程Embed模型: {protocol}")
            embedding = OpenAIEmbeddings(
                model=model_name,
                api_key=model_api_key,
                base_url=model_base_url,
            )
            return embedding
