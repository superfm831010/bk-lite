import os

from dotenv import load_dotenv
from loguru import logger

from src.ocr.olm_ocr import OlmOcr


def test_olm_ocr():
    try:
        ocr = OlmOcr(base_url=os.getenv('TEST_INFERENCE_BASE_URL'),
                     api_key=os.getenv('TEST_INFERENCE_TOKEN'),
                     model="olmOCR")

        result = ocr.predict('/Users/umr/Desktop/1.png')
        logger.info(result)
    except Exception as e:
        logger.warning("olmOCR服务暂不可用")
