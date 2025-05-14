from typing import Dict

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool


@tool(parse_docstring=True)
def ansible_adhoc(config: RunnableConfig):
    pass


@tool(parse_docstring=True)
def ansible_playbook(config: RunnableConfig):
    pass
