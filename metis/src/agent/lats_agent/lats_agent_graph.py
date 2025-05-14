import logging
from typing import Literal, Union, Any, Dict

from langgraph.constants import END
from langgraph.graph import StateGraph
from loguru import logger

from src.agent.lats_agent.lats_agent_node import LatsAgentNode
from src.agent.lats_agent.lats_agent_state import LatsAgentState
from src.core.entity.basic_llm_response import BasicLLMResponse
from src.core.graph.tools_graph import ToolsGraph
from src.entity.agent.lats_agent_request import LatsAgentRequest
from src.entity.agent.lats_agent_response import LatsAgentResponse


def should_continue(state: LatsAgentState) -> Union[str, Literal["__end__"]]:
    """决定是否继续执行图中的下一步

    Args:
        state: 当前状态

    Returns:
        下一个节点名称或结束标记
    """
    root = state["root"]

    # 记录当前执行状态的关键信息
    logger.debug(f"搜索树高度: {root.height}, 是否解决: {root.is_solved}")

    # 如果找到解决方案，结束搜索
    if root.is_solved:
        logger.info("找到解决方案，结束搜索")
        return END

    # 如果搜索深度超过限制，结束搜索
    if root.height > LatsAgentNode.MAX_TREE_HEIGHT:
        logger.info(f"搜索深度达到上限 ({LatsAgentNode.MAX_TREE_HEIGHT})，结束搜索")
        return END

    # 继续探索
    return "expand"


class LatsAgentGraph(ToolsGraph):
    """LatsAgent 图执行器

    负责构建和执行 LatsAgent 的计算图，管理节点间的流转逻辑
    """

    async def compile_graph(self, request: LatsAgentRequest) -> StateGraph:
        """编译 LatsAgent 执行图

        Args:
            request: LatsAgent 请求参数

        Returns:
            构建好的状态图
        """
        logger.info("开始编译 LatsAgent 执行图")

        # 初始化节点构建器
        node_builder = LatsAgentNode()
        await node_builder.setup(request)

        # 创建状态图
        graph_builder = StateGraph(LatsAgentState)

        # 添加基础节点
        last_edge = self.prepare_graph(graph_builder, node_builder)
        logger.debug(f"基础图构建完成，最后一个边为: {last_edge}")

        # 添加 LatsAgent 特有节点
        graph_builder.add_node("generate_initial_response",
                               node_builder.generate_initial_response)
        graph_builder.add_node("expand", node_builder.expand)

        # 构建边和条件流转
        graph_builder.add_edge(last_edge, 'generate_initial_response')

        # 添加条件边，使用统一的控制函数
        for node_name in ["generate_initial_response", "expand"]:
            graph_builder.add_conditional_edges(
                node_name,
                should_continue,
                ["expand", END]
            )

        # 编译图
        graph = graph_builder.compile()
        logger.info("LatsAgent 执行图编译完成")

        return graph

    async def stream(self, request: LatsAgentRequest) -> Any:
        """以流式方式执行 LatsAgent

        Args:
            request: LatsAgent 请求参数

        Returns:
            流式执行结果
        """
        logger.info(
            f"开始流式执行 LatsAgent，用户ID: {request.user_id}, 线程ID: {request.thread_id}")

        graph = await self.compile_graph(request)
        result = await self.invoke(graph, request, stream_mode='messages')

        logger.info("LatsAgent 流式执行完成")
        return result

    async def execute(self, request: LatsAgentRequest) -> LatsAgentResponse:
        """执行 LatsAgent 并返回结果

        Args:
            request: LatsAgent 请求参数

        Returns:
            执行结果
        """
        logger.info(
            f"开始执行 LatsAgent，用户ID: {request.user_id}, 线程ID: {request.thread_id}")

        graph = await self.compile_graph(request)

        # 使用更高的递归限制以支持复杂计算
        config = {"recursion_limit": 30}
        result = await self.invoke(graph, request, config=config)

        # 构造响应
        llm_response = LatsAgentResponse(
            message=result.get('response', ""),
            metadata={
                "tree_height": result.get("root", {}).height if "root" in result else 0,
                "is_solved": result.get("root", {}).is_solved if "root" in result else False
            }
        )

        logger.info("LatsAgent 执行完成")
        return llm_response
