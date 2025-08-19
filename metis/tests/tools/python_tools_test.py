import logging

logger = logging.getLogger(__name__)

from src.core.tools import python_analyze_repl


def test_python_analyze_repl():
    result = python_analyze_repl.run("print('123')", config={
        'configurable': {
            'user_id': '1'
        }
    })
    logger.info(result)
