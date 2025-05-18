from src.loader.text_loader import TextLoader
import logging

logger = logging.getLogger(__name__)


def test_load_txt_full_mode():
    loader = TextLoader(path='tests/assert/full_text_loader.txt', load_mode='full')
    result = loader.load()
    logger.info(result)
