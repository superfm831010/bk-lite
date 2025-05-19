import logging

logger = logging.getLogger(__name__)

from src.ocr.pp_ocr import PPOcr


def test_pp_ocr():
    ocr = PPOcr()
    result = ocr.predict('./tests/assert/umr.jpeg')
    logger.info(result)
