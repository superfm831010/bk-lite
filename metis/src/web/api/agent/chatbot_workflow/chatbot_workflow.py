from sanic.log import logger
from sanic import Blueprint, json
from sanic_ext import validate
from src.core.agent.chatbot_workflow.chatbot_workflow_graph import ChatBotWorkflowGraph
from src.web.api.agent.chatbot_workflow.chatbot_workflow_sse_handler import chatbot_workflow_stream_response
from src.web.entity.agent.chatbot_workflow.chatbot_workflow_request import ChatBotWorkflowRequest
from src.web.services.agent_service import AgentService
from sanic.response import ResponseStream
from src.core.sanic_plus.auth.api_auth import auth

chatbot_workflow_api_router = Blueprint(
    "chatbot_workflow_api_router", url_prefix="/agent")


@chatbot_workflow_api_router.post("/invoke_chatbot_workflow")
@auth.login_required
@validate(json=ChatBotWorkflowRequest)
async def invoke_chatbot_workflow(request, body: ChatBotWorkflowRequest):
    workflow = ChatBotWorkflowGraph()
    AgentService.set_naive_rag_search_query(body)
    logger.debug(f"执行ChatBotWorkflowGraph,用户的问题:[{body.user_message}]")

    result = await workflow.execute(body)
    response_content = result.model_dump()
    logger.info(
        f"执行ChatBotWorkflowGraph成功,用户的问题:[{body.user_message}]，结果:[{response_content}]")

    return json(response_content)


@chatbot_workflow_api_router.post("/invoke_chatbot_workflow_sse")
@auth.login_required
@validate(json=ChatBotWorkflowRequest)
async def invoke_chatbot_workflow_sse(request, body: ChatBotWorkflowRequest):
    workflow = ChatBotWorkflowGraph()
    AgentService.set_naive_rag_search_query(body)
    logger.debug(f"执行ChatBotWorkflowGraph,用户的问题:[{body.user_message}]")

    return ResponseStream(
        lambda res: chatbot_workflow_stream_response(workflow, body, res),
        content_type="text/event-stream; charset=utf-8",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
