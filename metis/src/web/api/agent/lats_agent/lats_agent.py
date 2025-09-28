"""
LATS Agent 路由器 - 简化优化版本

提供简洁的 LATS Agent API 接口
优化代码结构，提升可读性和维护性
"""
from sanic.log import logger
from sanic import Blueprint, json
from sanic_ext import validate
from sanic.response import ResponseStream
import uuid

from src.core.agent.lats_agent.lats_agent_graph import LatsAgentGraph
from src.web.api.agent.lats_agent.lats_sse_handler import stream_lats_response
from src.core.sanic_plus.auth.api_auth import auth
from src.web.entity.agent.lats_agent.lats_agent_request import LatsAgentRequest
from src.web.services.agent_service import AgentService


lats_agent_router = Blueprint("lats_agent_router", url_prefix="/agent")


@lats_agent_router.post("/invoke_lats_agent")
@auth.login_required
@validate(json=LatsAgentRequest)
async def invoke_lats_agent(request, body: LatsAgentRequest):
    """
    调用 LATS Agent 同步接口

    返回完整的搜索结果
    """
    try:
        # 初始化 LATS 图和服务
        graph = LatsAgentGraph()
        AgentService.set_naive_rag_search_query(body)

        logger.info(f"执行 LATS Agent，用户问题: [{body.user_message}]")

        # 执行搜索
        result = await graph.execute(body)

        # 返回结果
        response_content = result.model_dump()
        logger.info(f"LATS Agent 执行成功，评分: {getattr(result, 'score', 'N/A')}")

        return json(response_content)

    except Exception as e:
        logger.error(f"LATS Agent 执行失败: {str(e)}", exc_info=True)
        return json({"error": "执行失败，请稍后重试"}, status=500)


@lats_agent_router.post("/invoke_lats_agent_sse")
@auth.login_required
@validate(json=LatsAgentRequest)
async def invoke_lats_agent_sse(request, body: LatsAgentRequest):
    """
    调用 LATS Agent 流式接口

    提供实时的搜索过程反馈
    """
    try:
        # 初始化组件
        workflow = LatsAgentGraph()
        AgentService.set_naive_rag_search_query(body)
        chat_id = str(uuid.uuid4())

        logger.info(
            f"启动 LATS Agent SSE，用户问题: [{body.user_message}], chat_id: {chat_id}")

        # 返回流式响应
        return ResponseStream(
            lambda res: stream_lats_response(
                workflow, body, chat_id, body.model, res),
            content_type="text/event-stream; charset=utf-8",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*"
            }
        )

    except Exception as e:
        logger.error(f"LATS Agent SSE 启动失败: {str(e)}", exc_info=True)
        return json({"error": "启动失败，请稍后重试"}, status=500)
