from datetime import datetime
import uuid
import json as json_util
from langchain_core.messages import AIMessageChunk, ToolMessage, AIMessage
from sanic.log import logger


async def react_agent_stream_response(workflow, body, res):
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
        if isinstance(chunk[0], (ToolMessage)):
            content = f"🔧 执行工具[{chunk[0].name}]\n\n"
            response_sse_obj = create_response_obj(
                delta_content=content)
            json_content = json_util.dumps(
                response_sse_obj, ensure_ascii=False)
            await res.write(f"data: {json_content}\n\n".encode('utf-8'))

        if isinstance(chunk[0], (AIMessage, AIMessageChunk)):
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
