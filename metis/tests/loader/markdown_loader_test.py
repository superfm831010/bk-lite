import logging

logger = logging.getLogger(__name__)

from src.core.loader import MarkdownLoader


def test_markdown_loader():
    loader = MarkdownLoader(path='../readme.md')
    rs = loader.load()
    logger.info(rs)
