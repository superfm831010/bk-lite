from langgraph.constants import END
from langgraph.graph import StateGraph
from sanic.log import logger

from src.core.agent.plan_and_execute_agent.plan_and_execute_agent_node import PlanAndExecuteAgentNode
from src.core.agent.plan_and_execute_agent.plan_and_execute_agent_state import PlanAndExecuteAgentState
from src.core.llm.graph.basic_graph import BasicGraph
from src.web.entity.agent.plan_and_execute_agent.plan_and_execute_agent_request import PlanAndExecuteAgentRequest


class PlanAndExecuteAgentGraph(BasicGraph):
    """Plan and Execute Agent的图实现 - 简化版本

    使用抽象的 ReAct 节点组合和 chat_node 大幅简化实现
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

        # 添加计划生成节点
        graph_builder.add_node("planner", node_builder.planner_node)

        # 使用 ReAct 组合节点处理计划执行和重新规划
        react_entry_node = node_builder.build_plan_execute_react_nodes(
            graph_builder=graph_builder,
            composite_node_name="plan_execute_agent",
            end_node=END
        )

        # 设置图边缘
        graph_builder.add_edge(last_edge, "planner")
        graph_builder.add_edge("planner", react_entry_node)

        # 编译图
        logger.info(f"编译Plan and Execute Agent图")
        graph = graph_builder.compile()
        return graph
