from typing import List

from src.core.entity.basic_llm_request import BasicLLMRequest
from src.core.entity.tools_server import ToolsServer


class LatsAgentRequest(BasicLLMRequest):
    tools_servers: List[ToolsServer] = []
    langchain_tools: List[str] = []
