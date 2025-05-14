from langchain_core.messages import AIMessage
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.core.entity.basic_llm_response import BasicLLMResponse
from src.core.graph.basic_graph import BasicGraph
from src.entity.agent.chatbot_workflow_request import ChatBotWorkflowRequest
from src.entity.agent.chatbot_workflow_response import ChatBotWorkflowResponse
from src.agent.chatbot_workflow.chatbot_workflow_node import ChatBotWorkflowNode
from src.agent.chatbot_workflow.chatbot_workflow_state import ChatBotWorkflowState
from langgraph.pregel import RetryPolicy


class ChatBotWorkflowGraph(BasicGraph):

    def compile_graph(self):
        graph_builder = StateGraph(ChatBotWorkflowState)
        node_builder = ChatBotWorkflowNode()

        last_edge = self.prepare_graph(graph_builder, node_builder)
        graph_builder.add_node(
            "chatbot_node", node_builder.chatbot_node, retry=RetryPolicy(max_attempts=5))

        graph_builder.add_edge(last_edge, "chatbot_node")
        graph_builder.add_edge("chatbot_node", END)

        graph = graph_builder.compile()
        return graph

    async def stream(self, request: ChatBotWorkflowRequest):
        graph = self.compile_graph()
        result = self.invoke(graph, request, stream_mode='messages')
        return result

    def execute(self, request: ChatBotWorkflowRequest) -> ChatBotWorkflowResponse:
        graph = self.compile_graph()
        result = self.invoke(graph, request)
        prompt_token = 0
        completion_token = 0

        for i in result["messages"]:
            if type(i) == AIMessage and 'token_usage' in i.response_metadata:
                prompt_token += i.response_metadata['token_usage']['prompt_tokens']
                completion_token += i.response_metadata['token_usage']['completion_tokens']
        response = BasicLLMResponse(message=result["messages"][-1].content,
                                    total_tokens=prompt_token + completion_token,
                                    prompt_tokens=prompt_token,
                                    completion_tokens=completion_token)

        return response
