from sanic.log import logger
from sanic import Blueprint, json
from sanic_ext import validate
from src.core.agent.plan_and_execute_agent.plan_and_execute_agent_graph import PlanAndExecuteAgentGraph
from src.web.api.agent.plan_and_execute_agent.plan_execute_sse_handler import stream_plan_execute_response
from src.web.api.agent.plan_and_execute_agent.plan_execute_response_formatter import PlanExecuteResponseFormatter
from src.core.sanic_plus.auth.api_auth import auth
from src.web.entity.agent.plan_and_execute_agent.plan_and_execute_agent_request import PlanAndExecuteAgentRequest
from src.web.services.agent_service import AgentService
from sanic.response import ResponseStream

plan_and_execute_agent_router = Blueprint(
    "plan_and_execute_agent_router", url_prefix="/agent")


@plan_and_execute_agent_router.post("/invoke_plan_and_execute_agent")
@auth.login_required
@validate(json=PlanAndExecuteAgentRequest)
async def invoke_plan_and_execute_agent(request, body: PlanAndExecuteAgentRequest):
    """
    Plan and Execute Agent 同步执行接口

    返回格式化后的执行结果，包含执行摘要和清晰的最终答案
    """
    graph = PlanAndExecuteAgentGraph()
    AgentService.set_naive_rag_search_query(body)

    logger.debug(f"执行PlanAndExecuteAgentGraph，用户的问题：[{body.user_message}]")
    result = await graph.execute(body)

    # 使用格式化器美化响应
    formatted_response = PlanExecuteResponseFormatter.format_response(result)

    logger.info(
        f"执行PlanAndExecuteAgentGraph成功，用户的问题：[{body.user_message}]，"
        f"执行步骤：{formatted_response.get('execution_summary', {}).get('completed_steps', 0)}步"
    )
    return json(formatted_response)


@plan_and_execute_agent_router.post("/invoke_plan_and_execute_agent_sse")
@auth.login_required
@validate(json=PlanAndExecuteAgentRequest)
async def invoke_plan_and_execute_agent_sse(request, body: PlanAndExecuteAgentRequest):
    """
    优雅的 Plan and Execute Agent SSE 接口

    提供类似 Claude 的执行体验，包括：
    - 清晰的阶段划分（规划、执行、完成）
    - 优雅的进度显示
    - 简洁的工具调用反馈
    - 结构化的最终输出
    """
    workflow = PlanAndExecuteAgentGraph()
    AgentService.set_naive_rag_search_query(body)
    logger.debug(f"执行优雅的PlanAndExecuteAgentGraph，用户的问题：[{body.user_message}]")

    # 生成聊天ID
    import uuid
    chat_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"

    async def sse_stream(response):
        async for data in stream_plan_execute_response(workflow, body, chat_id):
            await response.write(data.encode('utf-8'))

    return ResponseStream(
        sse_stream,
        content_type="text/event-stream; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 Nginx 缓冲，确保实时流式传输
            "Content-Encoding": "identity"  # 确保不压缩内容
        }
    )
