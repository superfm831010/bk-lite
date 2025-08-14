"""
Plan and Execute Agent SSE 处理器

简化版实现，使用与其他工作正常的SSE相同的模式
"""
import asyncio
import json
from typing import Dict, Any, AsyncGenerator
from datetime import datetime

from sanic.log import logger


async def stream_plan_execute_response(
    workflow,
    body: Dict[str, Any],
    chat_id: str,
    model: str = "plan-execute"
) -> AsyncGenerator[str, None]:
    """
    流式处理 Plan and Execute Agent 响应
    使用简化的标准SSE格式
    """
    created = int(datetime.now().timestamp())
    
    try:
        logger.info(f"[Plan Execute SSE] 开始流式处理，chat_id: {chat_id}")
        
        async for chunk in workflow.stream(body):
            logger.debug(f"[Plan Execute SSE] 收到 chunk: {type(chunk)}")
            
            if not chunk or not isinstance(chunk, dict):
                continue
            
            # 处理每个节点的数据
            for node_name, node_data in chunk.items():
                content = _extract_meaningful_content(node_name, node_data)
                
                if content:
                    # 使用标准的OpenAI SSE格式
                    response = {
                        "id": chat_id,
                        "object": "chat.completion.chunk", 
                        "created": created,
                        "model": model,
                        "choices": [{
                            "delta": {
                                "role": "assistant",
                                "content": content
                            },
                            "index": 0,
                            "finish_reason": None
                        }]
                    }
                    
                    json_str = json.dumps(response, ensure_ascii=False, separators=(',', ':'))
                    sse_data = f"data: {json_str}\n\n"
                    
                    logger.debug(f"[Plan Execute SSE] 发送内容: {content[:50]}...")
                    yield sse_data
                    await asyncio.sleep(0.05)  # 短暂延迟确保流畅体验
        
        # 发送结束标志
        response = {
            "id": chat_id,
            "object": "chat.completion.chunk",
            "created": created, 
            "model": model,
            "choices": [{
                "delta": {},
                "index": 0,
                "finish_reason": "stop"
            }]
        }
        
        json_str = json.dumps(response, ensure_ascii=False, separators=(',', ':'))
        yield f"data: {json_str}\n\n"
        
        logger.info(f"[Plan Execute SSE] 流式处理完成，chat_id: {chat_id}")
        
    except Exception as e:
        logger.error(f"[Plan Execute SSE] 处理过程中出错: {str(e)}", exc_info=True)
        # 发送错误消息
        error_response = {
            "id": chat_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [{
                "delta": {
                    "role": "assistant", 
                    "content": f"处理过程中出现错误: {str(e)}"
                },
                "index": 0,
                "finish_reason": "stop"
            }]
        }
        json_str = json.dumps(error_response, ensure_ascii=False, separators=(',', ':'))
        yield f"data: {json_str}\n\n"


def _extract_meaningful_content(node_name: str, node_data: Any) -> str:
    """
    提取有意义的内容，过滤技术信息
    """
    content = ""
    
    try:
        if isinstance(node_data, dict):
            # 从messages中提取内容
            if "messages" in node_data and isinstance(node_data["messages"], list):
                for message in node_data["messages"]:
                    if isinstance(message, dict):
                        msg_content = message.get("content", "")
                        if isinstance(msg_content, str) and msg_content.strip():
                            # 简单过滤掉明显的技术内容
                            if not _is_technical_message(msg_content):
                                content = msg_content.strip()
                                break
            
            # 直接提取内容字段
            elif "content" in node_data:
                msg_content = node_data["content"]
                if isinstance(msg_content, str) and msg_content.strip():
                    if not _is_technical_message(msg_content):
                        content = msg_content.strip()
        
        elif isinstance(node_data, str) and node_data.strip():
            if not _is_technical_message(node_data):
                content = node_data.strip()
        
        # 为不同节点添加适当的前缀
        if content:
            if node_name == "agent":
                content = f"📋 规划: {content}"
            elif node_name == "act":
                content = f"⚡ 执行: {content}"
            elif node_name == "replan":
                content = f"🔄 重新规划: {content}"
        
        return content
        
    except Exception as e:
        logger.error(f"[Plan Execute SSE] 提取内容失败: {str(e)}")
        return ""


def _is_technical_message(content: str) -> bool:
    """
    判断是否是技术性消息，需要过滤
    """
    if not content:
        return True
    
    # 过滤条件
    technical_patterns = [
        "tool_call_id",
        "function_call", 
        "api_call",
        '"type":',
        '"role":',
        '"content":',
        "metadata",
        "usage_metadata",
        "response_metadata",
        "finish_reason",
        '{"id":',
        '{"object":',
        "uuid-",
        "timestamp"
    ]
    
    content_lower = content.lower()
    
    # 检查是否包含技术模式
    for pattern in technical_patterns:
        if pattern in content_lower:
            return True
    
    # 过滤太短的内容
    if len(content.strip()) < 5:
        return True
    
    # 过滤纯JSON格式
    if content.strip().startswith('{') and content.strip().endswith('}'):
        try:
            json.loads(content)
            return True  # 是有效JSON，认为是技术消息
        except:
            pass
    
    return False
