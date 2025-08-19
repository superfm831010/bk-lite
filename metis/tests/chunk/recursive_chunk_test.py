import logging

logger = logging.getLogger(__name__)

from src.core.chunk.recursive_chunk import RecursiveChunk
from src.core.loader import TextLoader


def test_recursive_chunk():
    chunk = RecursiveChunk()
    loader = TextLoader(path='./tests/assert/full_text_loader.txt',load_mode='full')
    docs = loader.load()
    rs = chunk.chunk(docs)
    logger.info(rs)
