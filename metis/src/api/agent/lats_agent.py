from sanic.log import logger
from sanic import Blueprint, json
from sanic_ext import validate
from src.agent.lats_agent.lats_agent_graph import LatsAgentGraph
from src.api.agent.utils import stream_response
from src.core.sanic_plus.auth.api_auth import auth
from src.entity.agent.lats_agent.lats_agent_request import LatsAgentRequest
from src.services.agent_service import AgentService
from sanic.response import ResponseStream

lats_agent_router = Blueprint(
    "lats_agent_router", url_prefix="/agent")


@lats_agent_router.post("/invoke_lats_agent")
@auth.login_required
@validate(json=LatsAgentRequest)
async def invoke_lats_agent(request, body: LatsAgentRequest):
    graph = LatsAgentGraph()
    AgentService.set_naive_rag_search_query(body)

    logger.debug(f"执行LatsAgentGraph,用户的问题:[{body.user_message}]")
    result = await graph.execute(body)

    response_content = result.model_dump()
    logger.info(
        f"执行LatsAgentGraph成功，用户的问题:[{body.user_message}],结果:[{response_content}]")
    return json(response_content)


@lats_agent_router.post("/invoke_lats_agent_sse")
@auth.login_required
@validate(json=LatsAgentRequest)
async def invoke_lats_agent_sse(request, body: LatsAgentRequest):
    workflow = LatsAgentGraph()
    AgentService.set_naive_rag_search_query(body)
    logger.debug(f"执行LatsAgentGraph,用户的问题:[{body.user_message}]")

    return ResponseStream(
        lambda res: stream_response(workflow, body, res),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
