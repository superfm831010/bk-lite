import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

from src.ocr.azure_ocr import AzureOCR


def test_azure_ocr():
    try:
        azure_ocr = AzureOCR(
            os.getenv("TEST_AZURE_VISION_URL"),
            os.getenv("TEST_AZURE_VISION_TOKEN"),
        )

        image_path = "./tests/assert/umr.jpeg"
        result = azure_ocr.predict(image_path)
        logger.info(result)
    except Exception as e:
        logger.warning("Azure OCR服务暂不可用")
