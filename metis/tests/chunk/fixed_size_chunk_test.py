import logging

logger = logging.getLogger(__name__)

from src.core.chunk.fixed_size_chunk import FixedSizeChunk
from src.core.loader import TextLoader


def test_fixed_size_chunk():
    chunk = FixedSizeChunk()
    loader = TextLoader(path='./tests/assert/full_text_loader.txt')
    docs = loader.load()
    rs = chunk.chunk(docs)
    logger.info(rs)
