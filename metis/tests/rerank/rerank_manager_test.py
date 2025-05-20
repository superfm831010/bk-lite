from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)

from src.rerank.rerank_manager import ReRankManager


def test_rerank():
    result = ReRankManager.rerank(
        "local:bce:maidalun1020/bce-reranker-base_v1",
        "你好",
        [
            Document(page_content="你好呀"),
            Document(page_content="今天天气真好"),
            Document(page_content="你吃饭了吗"),
        ]
    )
    logger.info(result)
