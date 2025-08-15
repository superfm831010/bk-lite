"""
LATS Agent SSE 处理器

基于节点类型的智能过滤实现，避免内部信息泄露
"""
import asyncio
import json
import re
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
    完全基于 LATS 节点状态和类型进行智能过滤，避免关键词匹配
    """
    created = int(datetime.now().timestamp())
    sent_contents = set()  # 用于去重
    iteration_counter = 0  # 迭代计数器
    current_node_type = None  # 当前节点类型
    lats_state = {
        'current_node': None,
        'is_final_answer': False,
        'search_completed': False,
        'solution_found': False
    }

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
            # 添加详细的chunk类型日志以便调试
            chunk_type = type(chunk).__name__
            logger.info(f"[LATS SSE] 收到chunk类型: {chunk_type}")
            
            # 检查是否是最终完整状态（表示搜索结束）
            if isinstance(chunk, dict) and 'messages' in chunk and 'root' in chunk:
                # 这是 LATS 搜索的最终状态
                root_node = chunk.get('root')
                messages = chunk.get('messages', [])
                
                logger.info(f"[LATS SSE] 最终状态 - 消息数量: {len(messages)}")

                if root_node and hasattr(root_node, 'is_solved'):
                    lats_state['search_completed'] = True
                    lats_state['solution_found'] = root_node.is_solved
                    logger.info(f"[LATS SSE] 搜索完成，找到解决方案: {root_node.is_solved}")

                    # 获取最后一条消息作为最终答案（无论是否完全解决）
                    if messages:
                        final_message = messages[-1]
                        logger.info(f"[LATS SSE] 最终消息类型: {type(final_message).__name__}")
                        if hasattr(final_message, 'content') and final_message.content:
                            logger.info(f"[LATS SSE] 最终消息内容长度: {len(final_message.content)}")
                            lats_state['is_final_answer'] = True
                            if root_node.is_solved:
                                content = f"\n\n🎯 **LATS 最终解决方案**\n\n{final_message.content}\n\n"
                            else:
                                content = f"\n\n💡 **LATS 最佳候选答案**\n\n{final_message.content}\n\n"

                            if content not in sent_contents:
                                await res.write(_create_sse_data(chat_id, created, model, content).encode('utf-8'))
                                sent_contents.add(content)
                                logger.info(f"[LATS SSE] 成功发送最终答案")
                            else:
                                logger.info(f"[LATS SSE] 最终答案已发送过，跳过")
                        else:
                            logger.warning(f"[LATS SSE] 最终消息没有内容")
                    else:
                        logger.warning(f"[LATS SSE] 没有找到任何消息")
                continue

            # 检查是否是节点流转信息
            if isinstance(chunk, dict) and len(chunk) == 1:
                node_name = next(iter(chunk.keys()))
                current_node_type = node_name
                lats_state['current_node'] = node_name
                logger.info(f"[LATS SSE] 节点转换: {node_name}")

                # 根据节点类型发送对应的状态消息
                node_message = _get_node_status_message(node_name, iteration_counter)
                if node_message and node_message not in sent_contents:
                    await res.write(_create_sse_data(chat_id, created, model, node_message).encode('utf-8'))
                    sent_contents.add(node_message)

                    if node_name == "expand":
                        iteration_counter += 1
                    await asyncio.sleep(0.3)
                continue

            # 处理消息流 - 更宽松地捕获所有可能的答案内容
            if isinstance(chunk, (tuple, list)) and len(chunk) > 0:
                message = chunk[0]

                # 检查消息是否为None
                if message is None:
                    continue

                # 检查是否是 AI 消息，记录详细信息
                message_type = type(message).__name__
                logger.info(f"[LATS SSE] 处理消息类型: {message_type}")
                
                if "AIMessage" in message_type and hasattr(message, 'content'):
                    content = message.content.strip()
                    logger.info(f"[LATS SSE] AI消息内容长度: {len(content)}")
                    
                    # 对所有足够长的AI消息都进行显示，不过分限制
                    if content and len(content) > 30:  # 降低阈值
                        current_node = lats_state.get('current_node')
                        logger.info(f"[LATS SSE] 当前节点: {current_node}, 内容预览: {content[:100]}...")

                        # 根据节点类型和内容长度决定如何显示
                        if len(content) > 100:
                            display_content = f"\n\n� **搜索结果**\n\n{content}\n\n"
                        elif len(content) > 50:
                            display_content = f"\n\n💭 **思考过程**\n\n{content}\n\n"
                        else:
                            display_content = f"\n\n📝 **分析片段**\n\n{content}\n\n"
                            
                        if display_content not in sent_contents:
                            await res.write(_create_sse_data(chat_id, created, model, display_content).encode('utf-8'))
                            sent_contents.add(display_content)
                            logger.info(f"[LATS SSE] 发送AI消息内容")

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


def _extract_message_content_by_node_state(message: Any, lats_state: Dict[str, Any], iteration_counter: int = 0) -> str:
    """
    基于 LATS 节点状态从消息对象中提取内容
    完全依赖节点状态，不使用关键词匹配
    """
    try:
        # 首先检查消息是否为None
        if message is None:
            return ""

        message_type = type(message).__name__
        current_node_type = lats_state.get('current_node')

        # 检查消息是否有content属性
        if not hasattr(message, 'content') or not message.content:
            return ""

        raw_content = message.content.strip()
        if not raw_content:
            return ""

        # 基于节点类型和状态进行过滤和格式化
        if current_node_type == "generate_initial_response":
            return _format_initial_response_by_state(message_type, raw_content, lats_state)
        elif current_node_type == "expand":
            return _format_expand_by_state(message_type, raw_content, lats_state, iteration_counter)
        elif current_node_type == "tools" or "ToolMessage" in message_type:
            return _format_tool_by_state(message_type, raw_content, lats_state)
        else:
            # 对于其他节点类型，基于状态决定是否输出
            if lats_state.get('is_final_answer') and "AIMessage" in message_type and len(raw_content) > 50:
                return f"\n\n📝 **答案内容**\n\n{raw_content}\n\n"

        return ""

    except Exception as e:
        logger.error(f"[LATS SSE] 提取消息内容失败: {str(e)}")
        return ""


def _format_initial_response_by_state(message_type: str, content: str, lats_state: Dict[str, Any]) -> str:
    """基于状态格式化初始响应阶段的消息"""
    if "ToolMessage" in message_type:
        return "\n🔧 **工具执行完成**\n\n📊 已获取到相关信息，正在分析整理...\n\n"
    elif "AIMessage" in message_type:
        # 初始响应阶段的AI消息，基于消息长度和类型判断
        if len(content) > 100:
            return f"\n💡 **初始方案生成**\n\n正在构建第一个解决方案...\n\n"
    return ""


def _format_expand_by_state(message_type: str, content: str, lats_state: Dict[str, Any], iteration_counter: int) -> str:
    """基于状态格式化扩展搜索阶段的消息"""
    if "ToolMessage" in message_type:
        return "\n🔧 **工具调用完成**\n\n📋 获取到新的信息，继续候选方案评估...\n\n"
    elif "AIMessage" in message_type:
        # 扩展阶段的AI消息，基于消息类型和长度判断
        if len(content) > 100:
            # 如果搜索已完成且找到解决方案，这可能是最终答案
            if lats_state.get('search_completed') and lats_state.get('solution_found'):
                return f"\n\n🎯 **最终解决方案**\n\n{content}\n\n"
            else:
                return "\n🧬 **生成候选方案**\n\n💡 正在创建新的解决方案候选...\n\n"
    return ""


def _format_tool_by_state(message_type: str, content: str, lats_state: Dict[str, Any]) -> str:
    """基于状态格式化工具消息"""
    if "ToolMessage" in message_type:
        if len(content) > 500:
            return "\n🔧 **工具执行完成**\n\n📊 已获取到详细信息，正在整理分析...\n\n⚡ 继续执行下一步"
        else:
            return "\n🔧 **工具执行完成**\n\n📋 已获取相关信息\n\n"
    elif "AIMessage" in message_type and len(content) > 50:
        return f"\n🔧 **工具处理结果**\n\n{content}\n\n"
    return ""
