import os

from langchain_openai import OpenAIEmbeddings
import logging

logger = logging.getLogger(__name__)

from src.embed.embed_builder import EmbedBuilder


def test_fast_embed():
    embed = EmbedBuilder.get_embed(
        "local:huggingface_embedding:BAAI/bge-small-zh-v1.5")
    result = embed.embed_documents([
        "你好"
    ])
    logger.info(list(result))


def test_remote_embed():
    try:
        client = OpenAIEmbeddings(
            model=os.getenv('TEST_BCE_EMBED_MODEL'),
            api_key=os.getenv('TEST_INFERENCE_TOKEN'),
            base_url=os.getenv('TEST_INFERENCE_BASE_URL'),
        )
        responses = client.embed_documents([
            "介绍"
        ])

        logger.info(responses)

    except Exception as e:
        logger.warning("Embedding服务暂不可用")
