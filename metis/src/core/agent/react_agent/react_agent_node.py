from typing import Literal
from langchain_core.runnables import RunnableConfig
from sanic.log import logger

from src.core.llm.node.tools_node import ToolsNodes
from src.core.agent.react_agent.react_agent_state import ReActAgentState


class ReActAgentNode(ToolsNodes):
    """ReAct Agent 节点处理器 - 使用可复用的 ReAct 节点组合"""

    def __init__(self) -> None:
        super().__init__()

    async def setup(self, request) -> None:
        """初始化节点"""
        await super().setup(request)

    # 为了保持兼容性，保留原有的节点方法名称，但委托给基类的 ReAct 实现
    async def llm_node(self, state: ReActAgentState, config: RunnableConfig) -> ReActAgentState:
        """LLM 推理节点 - 委托给基类的 ReAct LLM 实现"""
        graph_request = config["configurable"]["graph_request"]
        system_prompt = getattr(graph_request, 'system_message_prompt', None)
        return await self._react_llm_node_impl(state, config, system_prompt)

    async def tool_node(self, state: ReActAgentState, config: RunnableConfig) -> ReActAgentState:
        """工具执行节点 - 委托给基类的 ReAct 工具实现"""
        tools_node = await self.build_tools_node()
        return await self._react_tool_node_impl(state, config, tools_node)

    def should_continue(self, state: ReActAgentState) -> Literal["tools", "end"]:
        """判断是否需要继续执行工具 - 委托给基类的 ReAct 条件判断"""
        return self._react_should_continue_impl(state, "tools", "end")
