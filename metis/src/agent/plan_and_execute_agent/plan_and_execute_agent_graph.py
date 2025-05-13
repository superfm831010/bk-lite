from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.pregel import RetryPolicy

from src.agent.plan_and_execute_agent.plan_and_execute_agent_node import PlanAndExecuteAgentNode
from src.agent.plan_and_execute_agent.plan_and_execute_agent_state import PlanAndExecuteAgentState
from src.core.entity.basic_llm_response import BasicLLMResponse
from src.core.graph.tools_graph import ToolsGraph
from src.entity.agent.plan_and_execute_agent_request import PlanAndExecuteAgentRequest
from src.entity.agent.plan_and_execute_agent_response import PlanAndExecuteAgentResponse
from src.entity.agent.react_agent_request import ReActAgentRequest
from src.entity.agent.react_agent_response import ReActAgentResponse


class PlanAndExecuteAgentGraph(ToolsGraph):

    async def compile_graph(self, request: PlanAndExecuteAgentRequest):
        node_builder = PlanAndExecuteAgentNode()

        await node_builder.setup(request)

        graph_builder = StateGraph(PlanAndExecuteAgentState)

        last_edge = self.prepare_graph(graph_builder, node_builder)

        graph_builder.add_node("agent", node_builder.execute_step, retry=RetryPolicy(max_attempts=5))
        graph_builder.add_node("planner", node_builder.plan_step)
        graph_builder.add_node("replan", node_builder.replan_step)

        graph_builder.add_edge(last_edge, "planner")

        graph_builder.add_edge("planner", "agent")
        graph_builder.add_edge("agent", "replan")
        graph_builder.add_conditional_edges(
            "replan",
            node_builder.should_end,
            ["agent", END],
        )

        graph = graph_builder.compile()
        return graph


    async def stream(self, request: PlanAndExecuteAgentRequest):
        graph = await self.compile_graph(request)
        result = await self.invoke(graph, request, stream_mode='messages')
        return result

    async def execute(self, request: PlanAndExecuteAgentRequest) -> PlanAndExecuteAgentResponse:
        graph = await self.compile_graph(request)
        result = await self.invoke(graph, request)
        llm_response = BasicLLMResponse(
            message=result['response'],
        )
        return llm_response
