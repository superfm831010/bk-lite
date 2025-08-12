from flask import request
from langchain_openai import OpenAIEmbeddings
from sanic.log import logger


class EmbedBuilder:
    _embed_instances = {}

    @classmethod
    def get_embed_instance(cls, protocol: str):
        if cls._embed_instances.get(protocol, None) is not None:
            return cls._embed_instances[protocol]

        model_type = protocol.split(':')[1]
        model_name = protocol.split(':')[2]

        if model_type == 'huggingface_embedding':
            from langchain_huggingface import HuggingFaceEmbeddings

            cls._embed_instances[protocol] = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': False},
                cache_folder="./models"
            )
            return cls._embed_instances[protocol]

        return None

    @staticmethod
    def get_embed(protocol: str, model_name: str = '', model_api_key: str = '', model_base_url: str = ''):
        if protocol.startswith('local:'):
            return EmbedBuilder.get_embed_instance(protocol)
        else:
            embeddings = OpenAIEmbeddings(
                model=model_name,
                api_key=model_api_key,
                base_url=model_base_url,
                request_timeout=60
            )
            return embeddings
