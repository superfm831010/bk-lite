"""
LATS Agent SSE 处理器

基于LATS Agent节点状态和类型的智能SSE输出处理

设计理念：
1. 完全基于LATS Agent的节点类型和状态进行输出控制
2. 避免关键词匹配，使用节点语义和状态判断
3. 根据不同节点的作用输出相应的用户友好信息
4. 确保只有真正的最终答案被输出给用户

支持的节点类型：
- generate_initial_response: 生成初始响应
- expand: 扩展搜索树，生成候选方案
- reflect: 反思评估（内部处理）
- select: 选择最佳方案（内部处理）
- tools: 工具调用处理
"""
import asyncio
import json
from typing import Dict, Any, Optional
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
    基于节点类型和状态进行智能输出控制
    """
    created = int(datetime.now().timestamp())
    sent_contents = set()  # 用于去重
    iteration_counter = 0  # 迭代计数器
    current_node_type = None  # 当前节点类型
    lats_state = {
        'is_searching': False,
        'has_initial_response': False,
        'search_iterations': 0,
        'final_solution_found': False
    }

    try:
        logger.info(f"[LATS SSE] 开始流式处理，chat_id: {chat_id}")

        # 发送搜索开始消息
        start_content = "🔍 **正在启动 LATS 智能搜索...**\n\n🧠 初始化语言辅助树搜索引擎\n\n💡 准备生成多个候选解决方案并进行深度搜索"
        await _send_sse_data(res, chat_id, created, model, start_content)
        sent_contents.add(start_content)
        await asyncio.sleep(0.3)

        # 获取流式迭代器
        stream_iter = await workflow.stream(body)

        async for chunk in stream_iter:
            logger.debug(f"[LATS SSE] 收到 chunk: {chunk}")

            # 处理节点转换
            if isinstance(chunk, dict) and len(chunk) == 1:
                node_name = next(iter(chunk.keys()))
                current_node_type = node_name
                logger.debug(f"[LATS SSE] 节点转换: {node_name}")

                # 根据节点类型更新状态和发送消息
                await _handle_node_transition(
                    node_name, lats_state, iteration_counter,
                    res, chat_id, created, model, sent_contents
                )

                if node_name == "expand":
                    iteration_counter += 1
                    lats_state['search_iterations'] = iteration_counter
                continue

            # 处理消息流
            if isinstance(chunk, (tuple, list)) and len(chunk) > 0:
                message = chunk[0]

                if message is None:
                    continue

                # 基于节点类型和状态处理消息
                content = await _process_node_message(
                    message, current_node_type, lats_state, iteration_counter
                )

                if content and content not in sent_contents:
                    await _send_sse_data(res, chat_id, created, model, content)
                    sent_contents.add(content)
                    logger.info(f"[LATS SSE] 发送内容: {content[:50]}...")
                    await _adaptive_delay(content)

        # 发送搜索完成消息
        if lats_state['final_solution_found']:
            completion_content = "\n\n---\n\n✨ **LATS 搜索成功完成！**\n\n🎉 已找到最佳解决方案\n\n💫 希望我的回答对您有帮助"
        else:
            completion_content = "\n\n---\n\n✨ **LATS 搜索完成！**\n\n🎉 已完成深度搜索和多候选方案评估\n\n💫 基于当前最佳方案为您提供回答"

        await _send_sse_data(res, chat_id, created, model, completion_content)

        # 发送结束标志
        await _send_end_signal(res, chat_id, created, model)
        logger.info(f"[LATS SSE] 流式处理完成，chat_id: {chat_id}")

    except Exception as e:
        logger.error(f"[LATS SSE] 处理过程中出错: {str(e)}", exc_info=True)
        error_content = f"\n\n---\n\n❌ **LATS 搜索过程中遇到问题**\n\n🔧 **错误详情：**\n{str(e)}\n\n💡 **建议：**\n请稍后重试"
        await _send_sse_data(res, chat_id, created, model, error_content, finish_reason="stop")


async def _handle_node_transition(
    node_name: str,
    lats_state: Dict[str, Any],
    iteration_counter: int,
    res, chat_id: str, created: int, model: str,
    sent_contents: set
) -> None:
    """处理节点转换，发送适当的状态消息"""

    node_messages = {
        "generate_initial_response": "\n🌱 **生成初始解决方案**\n\n🎯 分析问题并构建第一个候选回答",
        "expand": f"\n\n---\n\n🌳 **搜索迭代 #{iteration_counter + 1}**\n\n🔍 探索搜索树新分支，优化候选解决方案",
        "tools": "\n🔧 **调用专业工具**\n\n⚙️ 执行必要的工具操作获取信息",
    }

    # 更新状态
    if node_name == "generate_initial_response":
        lats_state['has_initial_response'] = True
    elif node_name == "expand":
        lats_state['is_searching'] = True

    # 发送节点状态消息
    node_message = node_messages.get(node_name)
    if node_message and node_message not in sent_contents:
        await _send_sse_data(res, chat_id, created, model, node_message)
        sent_contents.add(node_message)
        await asyncio.sleep(0.3)


async def _process_node_message(
    message: Any,
    current_node_type: str,
    lats_state: Dict[str, Any],
    iteration_counter: int
) -> Optional[str]:
    """
    基于节点类型和状态处理消息
    避免关键词匹配，完全依赖节点语义
    """
    try:
        if not hasattr(message, 'content') or not message.content:
            return None

        message_type = type(message).__name__
        content = message.content.strip()

        if not content:
            return None

        logger.debug(
            f"[LATS SSE] 处理节点消息: {current_node_type}, 消息类型: {message_type}")

        # 基于节点类型处理
        if current_node_type == "generate_initial_response":
            return _handle_initial_response_message(message_type, content, lats_state)

        elif current_node_type == "expand":
            return _handle_expand_message(message_type, content, lats_state, iteration_counter)

        elif current_node_type == "tools":
            return _handle_tools_message(message_type, content, lats_state)

        # 对于其他节点或无明确节点的情况
        else:
            return _handle_general_message(message_type, content, lats_state)

    except Exception as e:
        logger.error(f"[LATS SSE] 处理节点消息失败: {str(e)}")
        return None


def _handle_initial_response_message(message_type: str, content: str, lats_state: Dict[str, Any]) -> Optional[str]:
    """处理初始响应节点的消息"""
    if "ToolMessage" in message_type:
        return "\n🔧 **初始信息收集完成**\n\n📊 正在分析获取的信息...\n"

    elif "AIMessage" in message_type:
        # 初始响应阶段的AI消息
        if _is_substantial_response(content):
            lats_state['has_initial_response'] = True
            return f"\n💡 **初始解决方案**\n\n{content}\n\n"
        elif len(content) > 30:
            return f"\n💡 **初始分析**\n\n{content}\n\n"

    return None


def _handle_expand_message(message_type: str, content: str, lats_state: Dict[str, Any], iteration_counter: int) -> Optional[str]:
    """处理扩展搜索节点的消息"""
    if "ToolMessage" in message_type:
        return f"\n🔧 **搜索迭代 #{iteration_counter} 工具调用完成**\n\n📋 获取到新信息，继续候选方案评估...\n"

    elif "AIMessage" in message_type:
        # 检查是否是JSON格式的内部评估数据
        if _is_internal_evaluation_data(content):
            # 内部评估数据，不输出
            logger.debug(f"[LATS SSE] 过滤内部评估数据: {content[:50]}...")
            return None

        # 检查是否是综合性的最终答案
        if _is_comprehensive_answer(content):
            lats_state['final_solution_found'] = True
            return f"\n\n🎯 **LATS 最终答案**\n\n{content}\n\n"

        # 检查是否是有意义的候选方案
        elif _is_substantial_response(content):
            return f"\n\n💡 **候选方案**\n\n{content}\n\n"

    return None


def _handle_tools_message(message_type: str, content: str, lats_state: Dict[str, Any]) -> Optional[str]:
    """处理工具调用节点的消息"""
    if "ToolMessage" in message_type:
        if len(content) > 500:
            return "\n🔧 **工具执行完成**\n\n📊 已获取详细信息，正在整理分析...\n"
        else:
            return "\n🔧 **工具执行完成**\n\n📋 已获取相关信息\n"

    elif "AIMessage" in message_type and _is_substantial_response(content):
        return f"\n🔧 **工具处理结果**\n\n{content}\n\n"

    return None


def _handle_general_message(message_type: str, content: str, lats_state: Dict[str, Any]) -> Optional[str]:
    """处理一般消息"""
    if "AIMessage" in message_type:
        # 过滤内部评估数据
        if _is_internal_evaluation_data(content):
            return None

        # 检查是否是有价值的回答
        if _is_comprehensive_answer(content):
            lats_state['final_solution_found'] = True
            return f"\n\n🎯 **解决方案**\n\n{content}\n\n"
        elif _is_substantial_response(content):
            return f"\n\n💬 **回答**\n\n{content}\n\n"

    return None


def _is_internal_evaluation_data(content: str) -> bool:
    """检查是否是内部评估数据（JSON格式的评分、反思等）"""
    content_stripped = content.strip()

    # 检查是否是JSON格式
    if (content_stripped.startswith('{') and content_stripped.endswith('}')) or \
       (content_stripped.startswith('[') and content_stripped.endswith(']')):

        # 检查是否包含评估相关的字段
        evaluation_fields = ["reflections",
                             "score", "found_solution", "evaluation"]
        content_lower = content.lower()

        if any(field in content_lower for field in evaluation_fields):
            return True

    return False


def _is_comprehensive_answer(content: str) -> bool:
    """检查是否是综合性的最终答案"""
    # 基于内容长度和结构完整性判断
    if len(content) < 50:
        return False

    # 检查是否包含多种类型的信息（说明是综合性回答）
    content_indicators = [
        len([char for char in content if char in '。！？.!?']) >= 2,  # 包含多个句子
        '：' in content or ':' in content,  # 包含说明性内容
        len(content.split()) >= 15,  # 包含足够的词汇
        any(word in content for word in [
            '数据库', '系统', '产品', '技术', '解决方案', '介绍', '特点', '功能', '应用']),  # 包含实质性内容
        len(content) > 80,  # 内容长度足够
    ]

    # 如果满足多个指标，认为是综合性答案
    return sum(content_indicators) >= 3


def _is_substantial_response(content: str) -> bool:
    """检查是否是有实质内容的回答"""
    if len(content) < 10:
        return False

    # 排除明显的系统消息或提示
    system_indicators = [
        content.startswith('System:'),
        content.startswith('Human:'),
        content.startswith('Assistant:'),
        'tool_call' in content.lower(),
        'function_call' in content.lower(),
        content.strip().endswith('...'),  # 省略号结尾通常是不完整内容
        len(content.strip().split()) < 3,  # 词汇太少
    ]

    return not any(system_indicators)


async def _send_sse_data(res, chat_id: str, created: int, model: str, content: str, finish_reason: str = None) -> None:
    """发送SSE数据"""
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
    await res.write(f"data: {json_str}\n\n".encode('utf-8'))


async def _send_end_signal(res, chat_id: str, created: int, model: str) -> None:
    """发送结束信号"""
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


async def _adaptive_delay(content: str) -> None:
    """根据内容类型自适应延迟"""
    if "搜索迭代" in content or "候选解决方案" in content:
        await asyncio.sleep(0.4)
    elif "工具" in content or "调用" in content:
        await asyncio.sleep(0.3)
    elif "最终答案" in content or "解决方案" in content:
        await asyncio.sleep(0.2)
    else:
        await asyncio.sleep(0.1)
