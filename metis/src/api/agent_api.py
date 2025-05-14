import json as json_util
import uuid
from datetime import datetime

from langchain_core.messages import AIMessageChunk, ToolMessage
from loguru import logger
from sanic import Blueprint, json
from sanic.response import ResponseStream
from sanic_ext import validate

from src.agent.chatbot_workflow.chatbot_workflow_graph import ChatBotWorkflowGraph
from src.agent.react_agent.react_agent_graph import ReActAgentGraph
from src.core.web.api_auth import auth
from src.entity.agent.chatbot_workflow_request import ChatBotWorkflowRequest
from src.entity.agent.react_agent_request import ReActAgentRequest
from src.services.agent_service import AgentService

agent_api_router = Blueprint("agent", url_prefix="/agent")


async def stream_response(workflow, body, res):
    prompt_token = 0
    completion_token = 0
    created_time = int(datetime.now().timestamp())
    chat_id = str(uuid.uuid4())

    # 辅助函数：创建基础响应对象
    def create_response_obj(delta_content=None, finish_reason=None):
        response = {
            "id": chat_id,
            "object": "chat.completion.chunk",
            "created": created_time,
            "model": body.model,
            "prompt_tokens": prompt_token,
            "completion_tokens": completion_token,
            "total_tokens": prompt_token + completion_token,
            "choices": [
                {
                    "delta": {"role": "assistant"} if delta_content is None and finish_reason is None else {},
                    "index": 0,
                    "finish_reason": finish_reason
                }
            ]
        }

        # 如果有内容，添加到delta中
        if delta_content is not None:
            response["choices"][0]["delta"]["content"] = delta_content

        return response

    # 初始响应
    init_chunk = create_response_obj()
    await res.write(f"data: {json_util.dumps(init_chunk)}\n\n")

    result = await workflow.stream(body)

    async for chunk in result:
        if isinstance(chunk[0], (ToolMessage, AIMessageChunk)):
            content = chunk[0].content
            completion_token += workflow.count_tokens(content)

            # 根据消息类型设置不同的内容
            if isinstance(chunk[0], ToolMessage):
                tool_info = {
                    "tool_name": chunk[0].name,
                    "tool_result": chunk[0].content
                }
                delta_content = f"执行工具: {tool_info['tool_name']}\n工具执行结果: {tool_info['tool_result']}\n"
            else:  # AIMessageChunk
                delta_content = content

            # 使用辅助函数创建响应对象
            response_sse_obj = create_response_obj(delta_content=delta_content)
            json_content = json_util.dumps(response_sse_obj)
            await res.write(f"data: {json_content}\n\n")
        else:
            try:
                prompt_token += workflow.count_tokens(chunk[0].content)
            except Exception:
                pass

    # 最终响应
    final_chunk = create_response_obj(finish_reason="stop")
    await res.write(f"data: {json_util.dumps(final_chunk)}\n\n")
    await res.write("data: [DONE]\n\n")


@agent_api_router.post("/invoke_chatbot_workflow")
@auth.login_required
@validate(json=ChatBotWorkflowRequest)
async def invoke_chatbot_workflow(request, body: ChatBotWorkflowRequest):
    workflow = ChatBotWorkflowGraph()
    AgentService.set_naive_rag_search_query(body)
    logger.debug(f"执行ChatBotWorkflowGraph,用户的问题:[{body.user_message}]")
    result = workflow.execute(body)
    response_content = result.model_dump()
    logger.info(
        f"执行ChatBotWorkflowGraph成功,用户的问题:[{body.user_message}]，结果:[{response_content}]")
    return json(response_content)


@agent_api_router.post("/invoke_chatbot_workflow_sse")
@auth.login_required
@validate(json=ChatBotWorkflowRequest)
async def invoke_chatbot_workflow_sse(request, body: ChatBotWorkflowRequest):
    workflow = ChatBotWorkflowGraph()
    AgentService.set_naive_rag_search_query(body)
    logger.debug(f"执行ChatBotWorkflowGraph,用户的问题:[{body.user_message}]")

    return ResponseStream(
        lambda res: stream_response(workflow, body, res),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )


@agent_api_router.post("/invoke_react_agent")
@auth.login_required
@validate(json=ReActAgentRequest)
async def invoke_react_agent(request, body: ReActAgentRequest):
    graph = ReActAgentGraph()
    AgentService.set_naive_rag_search_query(body)

    logger.debug(f"执行ReActAgentGraph,用户的问题:[{body.user_message}]")
    result = await graph.execute(body)
    response_content = result.model_dump()
    logger.info(
        f"执行ReActAgentGraph成功，用户的问题:[{body.user_message}],结果:[{response_content}]")
    return json(response_content)


@agent_api_router.post("/invoke_react_agent_sse")
@auth.login_required
@validate(json=ReActAgentRequest)
async def invoke_react_agent_sse(request, body: ReActAgentRequest):
    workflow = ReActAgentGraph()
    AgentService.set_naive_rag_search_query(body)
    logger.debug(f"执行ReActAgentGraph,用户的问题:[{body.user_message}]")

    return ResponseStream(
        lambda res: stream_response(workflow, body, res),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
