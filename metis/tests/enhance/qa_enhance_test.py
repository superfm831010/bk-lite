import os

import logging

logger = logging.getLogger(__name__)

from src.enhance.qa_enhance import QAEnhance
from src.entity.rag.enhance.qa_enhance_request import QAEnhanceRequest


def test_qa_enhance():
    req = QAEnhanceRequest(
        size=10,
        content='今天天气不错',
        model="gpt-4o",
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    e = QAEnhance(req)

    qa = e.generate_qa()
    logger.info(qa)
