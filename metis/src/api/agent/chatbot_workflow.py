from datetime import datetime
import uuid
import json as json_util
from langchain_core.messages import AIMessageChunk, ToolMessage, AIMessage
from loguru import logger
from sanic import Blueprint, json
from sanic_ext import validate
from src.services.agent_service import AgentService
from sanic.response import ResponseStream
from neco.sanic.auth.api_auth import auth
from neco.llm.agent.chatbot_workflow import *


async def chatbot_workflow_stream_response(workflow, body, res):
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
    await res.write(f"data: {json_util.dumps(init_chunk, ensure_ascii=False)}\n\n".encode('utf-8'))

    result = await workflow.stream(body)

    async for chunk in result:
        if isinstance(chunk[0], (ToolMessage, AIMessage, AIMessageChunk)):
            content = chunk[0].content
            completion_token += workflow.count_tokens(content)

            response_sse_obj = create_response_obj(
                delta_content=content)
            json_content = json_util.dumps(
                response_sse_obj, ensure_ascii=False)
            await res.write(f"data: {json_content}\n\n".encode('utf-8'))
        else:
            try:
                prompt_token += workflow.count_tokens(chunk[0].content)
            except Exception:
                pass

    # 最终响应
    final_chunk = create_response_obj(finish_reason="stop")
    await res.write(f"data: {json_util.dumps(final_chunk, ensure_ascii=False)}\n\n".encode('utf-8'))
    await res.write("data: [DONE]\n\n".encode('utf-8'))


chatbot_workflow_api_router = Blueprint(
    "chatbot_workflow_api_router", url_prefix="/agent")


@chatbot_workflow_api_router.post("/invoke_chatbot_workflow")
@auth.login_required
@validate(json=ChatBotWorkflowRequest)
async def invoke_chatbot_workflow(request, body: ChatBotWorkflowRequest):
    workflow = ChatBotWorkflowGraph()
    AgentService.prepare_request(body)
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
    AgentService.prepare_request(body)
    logger.debug(f"执行ChatBotWorkflowGraph,用户的问题:[{body.user_message}]")

    return ResponseStream(
        lambda res: chatbot_workflow_stream_response(workflow, body, res),
        content_type="text/event-stream; charset=utf-8",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
