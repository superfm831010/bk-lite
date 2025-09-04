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
        logger.debug(f"接收到流式数据块: {type(chunk)}, 内容: {chunk}")
        
        # LangGraph astream 输出格式通常是 (node_name, output) 或者是包含 'messages' 的字典
        if isinstance(chunk, dict):
            # 处理字典格式的 chunk
            messages = chunk.get('messages', [])
            if messages:
                # 如果 messages 是列表，取最后一个
                if isinstance(messages, list):
                    for msg in messages:
                        if isinstance(msg, (ToolMessage, AIMessage, AIMessageChunk)) and hasattr(msg, 'content'):
                            content = msg.content
                            if content:
                                completion_token += workflow.count_tokens(content)
                                response_sse_obj = create_response_obj(delta_content=content)
                                json_content = json_util.dumps(response_sse_obj, ensure_ascii=False)
                                await res.write(f"data: {json_content}\n\n".encode('utf-8'))
                # 如果 messages 是单个消息对象
                elif isinstance(messages, (ToolMessage, AIMessage, AIMessageChunk)) and hasattr(messages, 'content'):
                    content = messages.content
                    if content:
                        completion_token += workflow.count_tokens(content)
                        response_sse_obj = create_response_obj(delta_content=content)
                        json_content = json_util.dumps(response_sse_obj, ensure_ascii=False)
                        await res.write(f"data: {json_content}\n\n".encode('utf-8'))
        elif isinstance(chunk, tuple) and len(chunk) >= 2:
            # 处理元组格式的 chunk，如 (node_name, output)
            node_name, output = chunk[0], chunk[1]
            logger.debug(f"节点 {node_name} 产生输出: {type(output)}")
            
            if isinstance(output, dict) and 'messages' in output:
                messages = output['messages']
                if isinstance(messages, (ToolMessage, AIMessage, AIMessageChunk)) and hasattr(messages, 'content'):
                    content = messages.content
                    if content:
                        completion_token += workflow.count_tokens(content)
                        response_sse_obj = create_response_obj(delta_content=content)
                        json_content = json_util.dumps(response_sse_obj, ensure_ascii=False)
                        await res.write(f"data: {json_content}\n\n".encode('utf-8'))
        else:
            # 处理其他格式，尝试解析为消息
            logger.debug(f"未识别的数据块格式: {type(chunk)}")
            try:
                if hasattr(chunk, 'content'):
                    prompt_token += workflow.count_tokens(chunk.content)
            except Exception as e:
                logger.warning(f"处理数据块时出错: {e}")

    # 最终响应
    final_chunk = create_response_obj(finish_reason="stop")
    await res.write(f"data: {json_util.dumps(final_chunk, ensure_ascii=False)}\n\n".encode('utf-8'))
    await res.write("data: [DONE]\n\n".encode('utf-8'))
