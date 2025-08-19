"""
LATS Agent 图执行器 - 简化优化版本

简化图构建逻辑，优化执行流程
保持核心功能的同时提升代码可读性
"""
from langgraph.constants import END
from langgraph.graph import StateGraph
from sanic.log import logger

from src.core.agent.lats_agent.lats_agent_node import LatsAgentNode
from src.core.agent.lats_agent.lats_agent_state import LatsAgentState
from src.core.llm.graph.tools_graph import ToolsGraph
from src.web.entity.agent.lats_agent.lats_agent_request import LatsAgentRequest


class LatsAgentGraph(ToolsGraph):
    """LATS Agent 图执行器 - 优化版本"""

    async def compile_graph(self, request: LatsAgentRequest) -> StateGraph:
        """编译 LATS Agent 执行图"""
        logger.info("🔧 编译 LATS Agent 执行图")

        # 初始化优化版本的节点构建器
        node_builder = LatsAgentNode()
        await node_builder.setup(request)

        # 创建状态图
        graph_builder = StateGraph(LatsAgentState)

        # 添加基础图结构
        last_edge = self.prepare_graph(graph_builder, node_builder)
        logger.debug(f"基础图构建完成，连接点: {last_edge}")

        # 添加 LATS 特有节点
        graph_builder.add_node("generate_initial_response",
                               node_builder.generate_initial_response)
        graph_builder.add_node("expand", node_builder.expand)
        graph_builder.add_node("generate_final_answer",
                               node_builder.generate_final_answer)

        # 构建执行流程
        graph_builder.add_edge(last_edge, 'generate_initial_response')

        # 添加条件边 - 优化的控制流程
        for node_name in ["generate_initial_response", "expand"]:
            graph_builder.add_conditional_edges(
                node_name,
                node_builder.should_continue,
                ["expand", "generate_final_answer"]
            )

        # 最终答案生成后结束
        graph_builder.add_edge("generate_final_answer", END)

        # 编译并返回图
        compiled_graph = graph_builder.compile()
        logger.info("✅ LATS Agent 执行图编译完成")

        return compiled_graph
