from langchain_core.messages import AIMessage
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.core.entity.basic_llm_request import BasicLLMReuqest
from src.core.entity.basic_llm_response import BasicLLMResponse
from src.core.graph.basic_graph import BasicGraph
from src.entity.agent.chatbot_workflow.chatbot_workflow_request import ChatBotWorkflowRequest
from src.entity.agent.chatbot_workflow.chatbot_workflow_response import ChatBotWorkflowResponse
from src.agent.chatbot_workflow.chatbot_workflow_node import ChatBotWorkflowNode
from src.agent.chatbot_workflow.chatbot_workflow_state import ChatBotWorkflowState
from langgraph.pregel import RetryPolicy


class ChatBotWorkflowGraph(BasicGraph):

    async def compile_graph(self, request: BasicLLMReuqest):
        graph_builder = StateGraph(ChatBotWorkflowState)
        node_builder = ChatBotWorkflowNode()

        last_edge = self.prepare_graph(graph_builder, node_builder)
        graph_builder.add_node(
            "chatbot_node", node_builder.chatbot_node, retry=RetryPolicy(max_attempts=5))

        graph_builder.add_edge(last_edge, "chatbot_node")
        graph_builder.add_edge("chatbot_node", END)

        graph = graph_builder.compile()
        return graph
