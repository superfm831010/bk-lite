from src.loader.excel_loader import ExcelLoader
import logging

logger = logging.getLogger(__name__)


def test_excel_loader():
    loader = ExcelLoader('tests/assert/excel_loader.xlsx', mode='full')
    rs = loader.load()
    logger.info(rs)


def test_excel_loader_title_row_struct_load():
    loader = ExcelLoader(
        'tests/assert/excel_loader_title_chunk.xlsx', mode='excel_header_row_parse')
    rs = loader.title_row_struct_load()
    logger.info(rs)
