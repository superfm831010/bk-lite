import operator
from typing import List, Annotated, Tuple

from pydantic import Field

from src.core.entity.basic_llm_request import BasicLLMRequest
from src.core.entity.tools_server import ToolsServer


class PlanAndExecuteAgentRequest(BasicLLMRequest):
    tools_servers: List[ToolsServer] = []
    langchain_tools: List[str] = []
