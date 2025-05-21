import os

from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

from src.ocr.olm_ocr import OlmOcr


def test_olm_ocr():
    try:
        ocr = OlmOcr(base_url=os.getenv('TEST_INFERENCE_BASE_URL'),
                     api_key=os.getenv('TEST_INFERENCE_TOKEN'),
                     model="olmOCR")

        result = ocr.predict('./tests/assert/umr.jpeg')
        logger.info(result)
    except Exception as e:
        logger.warning("olmOCR服务暂不可用")
