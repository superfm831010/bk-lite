import logging

logger = logging.getLogger(__name__)

from src.core.loader.image_loader import ImageLoader
from src.core.ocr.pp_ocr import PPOcr


def test_image_loader():
    loader = ImageLoader('tests/assert/umr.jpeg', PPOcr())
    rs = loader.load()
    logger.info(rs)
