from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy
from sanic.log import logger

from src.core.llm.graph.tools_graph import ToolsGraph
from src.web.entity.agent.react_agent.react_agent_request import ReActAgentRequest
from src.core.agent.react_agent.react_agent_node import ReActAgentNode
from src.core.agent.react_agent.react_agent_state import ReActAgentState


class ReActAgentGraph(ToolsGraph):
    """ReAct Agent 图执行器 - 使用可复用的 ReAct 节点组合"""

    async def compile_graph(self, request: ReActAgentRequest):
        """编译 ReAct Agent 执行图"""
        logger.info("🔧 编译 ReAct Agent 执行图 (使用可复用 ReAct 组合)")

        # 初始化节点构建器
        node_builder = ReActAgentNode()
        await node_builder.setup(request)

        # 创建状态图
        graph_builder = StateGraph(ReActAgentState)

        # 添加基础图结构（如果需要的话）
        last_edge = self.prepare_graph(graph_builder, node_builder)
        logger.debug(f"基础图构建完成，连接点: {last_edge}")

        # 使用可复用的 ReAct 节点组合构建图
        react_entry_node, should_continue_func = node_builder.build_react_nodes(
            graph_builder=graph_builder,
            llm_node_name="react_llm",
            tool_node_name="react_tools",
            system_prompt=getattr(request, 'system_message_prompt', None),
            end_node=END,
            tools_node=None  # 使用内部构建的工具节点
        )

        # 连接基础图到 ReAct 入口节点
        graph_builder.add_edge(last_edge, react_entry_node)

        # 编译并返回图
        compiled_graph = graph_builder.compile()
        logger.info("✅ ReAct Agent 执行图编译完成 (使用可复用组合)")

        return compiled_graph
