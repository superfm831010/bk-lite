from typing import Optional
from sanic.log import logger

from src.core.ocr.azure_ocr import AzureOCR
from src.core.ocr.olm_ocr import OlmOcr
from src.core.ocr.pp_ocr import PPOcr


class OcrManager:
    @classmethod
    def load_ocr(cls, ocr_type: str,
                 olm_base_url: Optional[str], olm_api_key: Optional[str], olm_model: Optional[str],
                 azure_base_url: Optional[str], azure_api_key: Optional[str]):
        ocr = None
        logger.debug(f"加载OCR服务，类型: {ocr_type}")

        if ocr_type == 'pp_ocr':
            logger.debug("初始化PP-OCR服务")
            ocr = PPOcr()

        if ocr_type == 'olm_ocr':
            logger.debug(f"初始化OLM-OCR服务，模型: {olm_model}")
            ocr = OlmOcr(base_url=olm_base_url,
                         api_key=olm_api_key, model=olm_model)

        if ocr_type == 'azure_ocr':
            logger.debug(f"初始化Azure-OCR服务，endpoint: {azure_base_url}")
            ocr = AzureOCR(api_key=azure_api_key, endpoint=azure_base_url)

        return ocr
