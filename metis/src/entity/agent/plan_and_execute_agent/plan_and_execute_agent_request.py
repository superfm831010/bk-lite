import operator
from typing import List, Annotated, Tuple

from pydantic import Field

from src.core.entity.basic_llm_request import BasicLLMReuqest
from src.core.entity.tools_server import ToolsServer


class PlanAndExecuteAgentRequest(BasicLLMReuqest):
    tools_servers: List[ToolsServer] = []
    langchain_tools:List[str] = []