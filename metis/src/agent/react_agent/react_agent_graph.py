from langchain_core.messages import AIMessage
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.core.entity.basic_llm_response import BasicLLMResponse
from src.core.graph.tools_graph import ToolsGraph
from src.entity.agent.react_agent.react_agent_request import ReActAgentRequest
from src.entity.agent.react_agent.react_agent_response import ReActAgentResponse
from src.agent.react_agent.react_agent_node import ReActAgentNode
from src.agent.react_agent.react_agent_state import ReActAgentState
from langgraph.pregel import RetryPolicy


class ReActAgentGraph(ToolsGraph):

    async def compile_graph(self, request: ReActAgentRequest):
        node_builder = ReActAgentNode()

        await node_builder.setup(request)

        graph_builder = StateGraph(ReActAgentState)

        last_edge = self.prepare_graph(graph_builder, node_builder)

        graph_builder.add_node("agent", node_builder.agent_node, retry=RetryPolicy(max_attempts=5))

        graph_builder.add_edge(last_edge, "agent")
        graph_builder.add_edge("agent", END)

        graph = graph_builder.compile()
        return graph
