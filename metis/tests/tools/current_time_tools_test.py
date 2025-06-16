import logging

logger = logging.getLogger(__name__)
from src.tools.current_time_tools import get_current_time


def test_current_time_tool_returns_string():
    result = get_current_time.run("", config={
        'configurable': {
            'user_id': '1'
        }
    })
    logger.info(result)
