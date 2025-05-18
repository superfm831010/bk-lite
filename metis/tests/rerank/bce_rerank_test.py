from src.rerank.bce_rerank import BCEReRank
import logging

logger = logging.getLogger(__name__)


def test_bce_rerank():
    rerank = BCEReRank()
    result = rerank.rerank("你好呀", [
        "你好", "今天天气真好", "你吃饭了吗"
    ])
    logger.info(result)
