"""
LATS Agent SSE 处理器

基于节点类型的智能过滤实现，避免内部信息泄露
"""
import asyncio
import json
from typing import Dict, Any
from datetime import datetime

from sanic.log import logger


async def stream_lats_response(
    workflow,
    body: Dict[str, Any],
    chat_id: str,
    model: str,
    res
):
    """
    流式处理 LATS Agent 响应
    简化逻辑，确保正确处理各种消息类型
    """
    created = int(datetime.now().timestamp())
    sent_contents = set()  # 用于去重
    iteration_counter = 0  # 迭代计数器
    current_node = None

    try:
        logger.info(f"[LATS SSE] 开始流式处理，chat_id: {chat_id}")

        # 发送优雅的开始消息
        start_content = "🔍 **正在启动 LATS 智能搜索...**\n\n🧠 初始化语言辅助树搜索引擎\n\n💡 准备生成多个候选解决方案并进行深度搜索"
        await res.write(_create_sse_data(chat_id, created, model, start_content).encode('utf-8'))
        sent_contents.add(start_content)
        await asyncio.sleep(0.3)

        # 获取流式迭代器
        stream_iter = await workflow.stream(body)

        async for chunk in stream_iter:
            logger.info(f"[LATS SSE] 收到chunk类型: {type(chunk).__name__}")

            # 检查是否是最终完整状态（表示搜索结束）
            if isinstance(chunk, dict) and 'messages' in chunk and 'root' in chunk:
                # 这是 LATS 搜索的最终状态
                root_node = chunk.get('root')
                messages = chunk.get('messages', [])

                if root_node and hasattr(root_node, 'is_solved'):
                    logger.info(
                        f"[LATS SSE] 搜索完成，找到解决方案: {root_node.is_solved}")

                    # 获取最后一条消息作为最终答案
                    if messages:
                        final_message = messages[-1]
                        logger.info(
                            f"[LATS SSE] 最终消息类型: {type(final_message).__name__}")
                        if hasattr(final_message, 'content') and final_message.content:
                            logger.info(
                                f"[LATS SSE] 最终消息内容长度: {len(final_message.content)}")
                            if root_node.is_solved:
                                content = f"\n\n🎯 **LATS 最终解决方案**\n\n{final_message.content}\n\n"
                            else:
                                content = f"\n\n💡 **LATS 最佳候选答案**\n\n{final_message.content}\n\n"

                            if content not in sent_contents:
                                await res.write(_create_sse_data(chat_id, created, model, content).encode('utf-8'))
                                sent_contents.add(content)
                                logger.info(f"[LATS SSE] 成功发送最终答案")
                continue

            # 检查是否是节点流转信息
            if isinstance(chunk, dict) and len(chunk) == 1:
                node_name = next(iter(chunk.keys()))
                current_node = node_name

                # 根据节点类型发送对应的状态消息
                node_message = _get_node_status_message(
                    node_name, iteration_counter)
                if node_message and node_message not in sent_contents:
                    await res.write(_create_sse_data(chat_id, created, model, node_message).encode('utf-8'))
                    sent_contents.add(node_message)

                    if node_name == "expand":
                        iteration_counter += 1
                continue

            # 处理消息流 - tuple/list 格式
            if isinstance(chunk, (tuple, list)) and len(chunk) > 0:
                message = chunk[0]
                logger.info(
                    f"[LATS SSE] 处理消息类型: {type(message).__name__ if message else 'None'}")

                # 检查消息是否为None
                if message is None:
                    continue

                # 获取消息类型和内容
                message_type = type(message).__name__
                content = ""

                # 处理不同类型的消息
                if hasattr(message, 'content') and message.content is not None:
                    # 对于流式消息，不要 strip，保持原始内容
                    if "Chunk" in type(message).__name__:
                        content = message.content  # 保持原始内容，包括空格
                    else:
                        content = message.content.strip()  # 只对完整消息进行 strip
                    logger.info(
                        f"[LATS SSE] 消息内容长度: {len(content)}, 原始内容: {repr(content)}")

                # 处理 AI 消息（包括 AIMessage 和 AIChunkMessage）
                if "AI" in message_type and "Message" in message_type:
                    # 对于 AIMessageChunk，直接流式转发
                    if "Chunk" in message_type:
                        # 流式消息直接转发，保持实时性，即使是空字符串也要发送
                        await res.write(_create_sse_data(chat_id, created, model, content).encode('utf-8'))
                        logger.info(
                            f"[LATS SSE] 转发AIChunkMessage: {repr(content)}")
                    elif content:  # 完整消息需要有实际内容
                        # 完整 AI 消息，根据内容长度决定显示方式
                        if len(content) > 5:  # 进一步降低阈值
                            if len(content) > 200:
                                display_content = f"\n\n📝 **详细分析**\n\n{content}\n\n"
                            elif len(content) > 100:
                                display_content = f"\n\n💭 **思考过程**\n\n{content}\n\n"
                            else:
                                display_content = f"\n\n🔍 **分析片段**\n\n{content}\n\n"

                            # 避免重复发送相同内容
                            content_hash = hash(content)
                            if content_hash not in sent_contents:
                                await res.write(_create_sse_data(chat_id, created, model, display_content).encode('utf-8'))
                                sent_contents.add(content_hash)
                                logger.info(
                                    f"[LATS SSE] 发送AI消息内容，类型: {message_type}")

                # 处理工具消息
                elif "Tool" in message_type and "Message" in message_type:
                    tool_content = "\n🔧 **工具执行完成**\n\n📊 已获取相关信息，正在分析...\n\n"
                    if tool_content not in sent_contents:
                        await res.write(_create_sse_data(chat_id, created, model, tool_content).encode('utf-8'))
                        sent_contents.add(tool_content)
                        logger.info(f"[LATS SSE] 发送工具消息")

                await asyncio.sleep(0.1)

        # 发送优雅的完成消息
        completion_content = "\n\n---\n\n✨ **LATS 搜索完成！**\n\n🎉 已完成深度搜索和多候选方案评估\n\n💫 希望我的回答对您有帮助"
        await res.write(_create_sse_data(chat_id, created, model, completion_content).encode('utf-8'))

        # 发送结束标志
        end_response = {
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

        json_str = json.dumps(
            end_response, ensure_ascii=False, separators=(',', ':'))
        await res.write(f"data: {json_str}\n\n".encode('utf-8'))
        await res.write("data: [DONE]\n\n".encode('utf-8'))

        logger.info(f"[LATS SSE] 流式处理完成，chat_id: {chat_id}")

    except Exception as e:
        logger.error(f"[LATS SSE] 处理过程中出错: {str(e)}", exc_info=True)
        # 发送优雅的错误消息
        error_content = f"\n\n---\n\n❌ **LATS 搜索过程中遇到问题**\n\n🔧 **错误详情：**\n{str(e)}\n\n💡 **建议：**\n请稍后重试，或联系技术支持获取帮助"
        await res.write(_create_sse_data(chat_id, created, model, error_content, finish_reason="stop").encode('utf-8'))


def _create_sse_data(chat_id: str, created: int, model: str, content: str, finish_reason: str = None) -> str:
    """创建SSE数据"""
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
            "finish_reason": finish_reason
        }]
    }

    json_str = json.dumps(response, ensure_ascii=False, separators=(',', ':'))
    return f"data: {json_str}\n\n"


def _get_node_status_message(node_name: str, iteration_counter: int) -> str:
    """根据节点类型获取状态消息"""
    node_messages = {
        "generate_initial_response": "\n🌱 **生成初始解决方案...**\n\n🎯 分析问题并构建第一个候选回答",
        "expand": f"\n\n---\n\n🌳 **搜索迭代 #{iteration_counter + 1}**\n\n🔍 正在探索搜索树的新分支，生成候选解决方案",
        "tools": "\n🔧 **调用专业工具...**\n\n⚙️ 执行必要的工具操作获取信息",
    }

    return node_messages.get(node_name, "")
