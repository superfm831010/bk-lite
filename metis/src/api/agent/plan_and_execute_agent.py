from sanic.log import logger
from sanic import Blueprint, json
from sanic_ext import validate
from src.agent.plan_and_execute_agent.plan_and_execute_agent_graph import PlanAndExecuteAgentGraph
from src.api.agent.utils import stream_response
from src.core.sanic_plus.auth.api_auth import auth
from src.entity.agent.plan_and_execute_agent.plan_and_execute_agent_request import PlanAndExecuteAgentRequest
from src.services.agent_service import AgentService
from sanic.response import ResponseStream

plan_and_execute_agent_router = Blueprint(
    "plan_and_execute_agent_router", url_prefix="/agent")


@plan_and_execute_agent_router.post("/invoke_plan_and_execute_agent")
@auth.login_required
@validate(json=PlanAndExecuteAgentRequest)
async def invoke_plan_and_execute_agent(request, body: PlanAndExecuteAgentRequest):
    graph = PlanAndExecuteAgentGraph()
    AgentService.set_naive_rag_search_query(body)

    logger.debug(f"执行PlanAndExecuteAgentGraph,用户的问题:[{body.user_message}]")
    result = await graph.execute(body)

    response_content = result.model_dump()
    logger.info(
        f"执行PlanAndExecuteAgentGraph成功，用户的问题:[{body.user_message}],结果:[{response_content}]")
    return json(response_content)


@plan_and_execute_agent_router.post("/invoke_plan_and_execute_agent_sse")
@auth.login_required
@validate(json=PlanAndExecuteAgentRequest)
async def invoke_plan_and_execute_agent_sse(request, body: PlanAndExecuteAgentRequest):
    workflow = PlanAndExecuteAgentGraph()
    AgentService.set_naive_rag_search_query(body)
    logger.debug(f"执行PlanAndExecuteAgentGraph,用户的问题:[{body.user_message}]")

    return ResponseStream(
        lambda res: stream_response(workflow, body, res),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
