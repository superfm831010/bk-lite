import logging

logger = logging.getLogger(__name__)

from src.core.loader import DocLoader
from src.core.ocr.pp_ocr import PPOcr

ocr = PPOcr()


def test_load_docs_full_mode():
    loader = DocLoader('tests/assert/pdf_word_raw.docx', mode='full', ocr=ocr)
    rs = loader.load()
    logger.info(rs)


def test_load_docs_paragraph_mode():
    loader = DocLoader('tests/assert/pdf_word_raw.docx',
                       mode='paragraph', ocr=ocr)
    rs = loader.load()
    logger.info(rs)
