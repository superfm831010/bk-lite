from typing import Dict

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool


@tool(parse_docstring=True)
def http_get_tool(param: str,config: RunnableConfig):
    """

    Args:
        param:

    Returns:

    """
    url = config['configurable']['url']

# post
# delete
# put