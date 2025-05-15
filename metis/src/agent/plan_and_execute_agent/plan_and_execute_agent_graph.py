from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.pregel import RetryPolicy
from loguru import logger

from src.agent.plan_and_execute_agent.plan_and_execute_agent_node import PlanAndExecuteAgentNode
from src.agent.plan_and_execute_agent.plan_and_execute_agent_state import PlanAndExecuteAgentState
from src.core.entity.basic_llm_response import BasicLLMResponse
from src.core.graph.tools_graph import ToolsGraph
from src.entity.agent.plan_and_execute_agent_request import PlanAndExecuteAgentRequest
from src.entity.agent.plan_and_execute_agent_response import PlanAndExecuteAgentResponse


class PlanAndExecuteAgentGraph(ToolsGraph):
    """Plan and Execute Agent的图实现

    负责构建和执行Plan and Execute智能体的工作流图
    """

    async def compile_graph(self, request: PlanAndExecuteAgentRequest):
        """编译工作流图

        Args:
            request: 计划执行代理请求

        Returns:
            编译后的图
        """
        # 创建节点构建器
        node_builder = PlanAndExecuteAgentNode()
        logger.info(f"初始化Plan and Execute Agent图，设置工具和请求")

        # 设置节点构建器
        await node_builder.setup(request)

        # 创建状态图
        graph_builder = StateGraph(PlanAndExecuteAgentState)
        logger.info(f"创建Plan and Execute Agent状态图")

        # 准备基本图结构
        last_edge = self.prepare_graph(graph_builder, node_builder)

        # 添加Plan and Execute特定节点
        graph_builder.add_node("agent", node_builder.execute_step,
                               retry=RetryPolicy(max_attempts=5))
        graph_builder.add_node("planner", node_builder.plan_step)
        graph_builder.add_node("replan", node_builder.replan_step)

        # 设置图边缘
        graph_builder.add_edge(last_edge, "planner")
        graph_builder.add_edge("planner", "agent")
        graph_builder.add_conditional_edges(
            "agent",
            node_builder.should_end,
            {
                "agent": "agent",  # 继续执行下一步
                "replan": "replan",  # 重新规划
                END: END,  # 结束执行
            }
        )
        graph_builder.add_conditional_edges(
            "replan",
            node_builder.should_end,
            {
                "agent": "agent",  # 继续执行新计划
                "replan": "replan",  # 继续重新规划
                END: END,  # 结束执行
            }
        )

        # 编译图
        logger.info(f"编译Plan and Execute Agent图")
        graph = graph_builder.compile()
        return graph

    async def stream(self, request: PlanAndExecuteAgentRequest):
        """流式执行图

        Args:
            request: 计划执行代理请求

        Returns:
            流式执行结果
        """
        logger.info(
            f"开始流式执行Plan and Execute Agent，请求: {request.user_message[:50]}...")
        graph = await self.compile_graph(request)
        result = await self.invoke(graph, request, stream_mode='messages')
        return result

    async def execute(self, request: PlanAndExecuteAgentRequest) -> PlanAndExecuteAgentResponse:
        """执行图并返回最终结果

        Args:
            request: 计划执行代理请求

        Returns:
            包含最终响应的对象
        """
        logger.info(
            f"开始执行Plan and Execute Agent，请求: {request.user_message[:50]}...")
        graph = await self.compile_graph(request)

        try:
            result = await self.invoke(graph, request)
            logger.info(f"Plan and Execute Agent执行完成")

            # 获取最终响应
            response = result.get('response', '')
            if not response and 'messages' in result:
                # 尝试从最后一条消息中获取响应
                last_messages = result.get('messages', [])
                if last_messages:
                    response = last_messages[-1].content

            # 创建响应对象
            llm_response = BasicLLMResponse(
                message=response,
            )
            return llm_response
        except Exception as e:
            logger.error(f"Plan and Execute Agent执行失败: {str(e)}")
            # 返回错误响应
            return BasicLLMResponse(
                message=f"执行任务时发生错误: {str(e)}",
                error=True
            )
