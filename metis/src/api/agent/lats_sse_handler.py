"""
LATS Agent SSE 处理器

基于节点类型的智能过滤和格式化实现，避免内部信息泄露

设计理念：
1. 优先使用节点类型（node type）作为格式化输出依据
2. 每个节点类型都有专门的格式化函数，确保输出的一致性
3. 通过节点类型而非内容匹配来决定输出格式，更加可靠
4. 支持扩展新的节点类型，只需添加对应的格式化函数

节点类型说明：
- generate_initial_response: 生成初始响应
- expand: 扩展搜索树
- tools: 工具调用
- reflect: 反思评估  
- select: 方案选择
- agent: 智能代理处理
- supervisor: 监督协调
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
    基于节点类型进行智能过滤，提供优雅的用户体验
    """
    created = int(datetime.now().timestamp())
    sent_contents = set()  # 用于去重
    iteration_counter = 0  # 迭代计数器
    current_node_type = None  # 当前节点类型

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
            logger.debug(f"[LATS SSE] 收到 chunk: {chunk}")

            # 检查是否是节点流转信息
            if isinstance(chunk, dict) and len(chunk) == 1:
                node_name = next(iter(chunk.keys()))
                current_node_type = node_name
                logger.debug(f"[LATS SSE] 切换到节点: {node_name}")

                # 根据节点类型发送对应的状态消息
                node_message = _get_node_status_message(
                    node_name, iteration_counter)
                if node_message and node_message not in sent_contents:
                    await res.write(_create_sse_data(chat_id, created, model, node_message).encode('utf-8'))
                    sent_contents.add(node_message)

                    if node_name == "expand":
                        iteration_counter += 1
                    await asyncio.sleep(0.3)
                continue

            # 处理消息流
            if isinstance(chunk, (tuple, list)) and len(chunk) > 0:
                message = chunk[0]

                # 检查消息是否为None
                if message is None:
                    logger.debug(f"[LATS SSE] 跳过None消息")
                    continue

                # 基于当前节点类型提取消息内容
                content = _extract_message_content_by_node(
                    message, current_node_type, iteration_counter)

                if content and content not in sent_contents:
                    # 使用标准的OpenAI SSE格式
                    await res.write(_create_sse_data(chat_id, created, model, content).encode('utf-8'))
                    sent_contents.add(content)
                    logger.info(f"[LATS SSE] 发送内容: {content[:50]}...")

                    # 根据内容类型调整延迟
                    if "搜索迭代" in content or "候选解决方案" in content:
                        await asyncio.sleep(0.4)
                    elif "评估" in content or "工具" in content:
                        await asyncio.sleep(0.3)
                    else:
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
    """根据节点类型获取状态消息，优先基于节点类型进行输出"""
    node_messages = {
        "generate_initial_response": "\n🌱 **生成初始解决方案...**\n\n🎯 分析问题并构建第一个候选回答",
        "expand": f"\n\n---\n\n🌳 **搜索迭代 #{iteration_counter + 1}**\n\n🔍 正在探索搜索树的新分支，生成候选解决方案",
        "tools": "\n🔧 **调用专业工具...**\n\n⚙️ 执行必要的工具操作获取信息",
        "reflect": "\n🤔 **反思与评估...**\n\n📈 分析当前方案的质量和有效性",
        "select": "\n🎯 **选择最佳方案...**\n\n⭐ 从多个候选方案中选择最优解",
        "agent": "\n🤖 **智能代理处理...**\n\n🧠 执行高级推理和决策",
        "supervisor": "\n👨‍💼 **监督节点...**\n\n📊 协调和监督整个搜索过程",
    }

    return node_messages.get(node_name, f"\n🔄 **执行节点: {node_name}**\n\n⚡ 正在处理...")


def _extract_message_content_by_node(message: Any, current_node_type: str, iteration_counter: int = 0) -> str:
    """
    基于当前节点类型从消息对象中提取和格式化内容
    优先使用节点类型作为格式化输出依据
    """
    try:
        # 首先检查消息是否为None
        if message is None:
            logger.debug(f"[LATS SSE] 消息为None，跳过处理")
            return ""

        message_type = type(message).__name__
        logger.debug(
            f"[LATS SSE] 处理消息类型: {message_type}, 当前节点: {current_node_type}")

        # 检查消息是否有content属性
        if not hasattr(message, 'content') or not message.content:
            return ""

        raw_content = message.content.strip()
        if not raw_content:
            return ""

        # 过滤内部信息，无论在哪个节点都不应该泄露
        if _contains_internal_keywords(raw_content):
            logger.debug(f"[LATS SSE] 过滤内部信息: {raw_content[:50]}...")
            return ""

        # 基于节点类型进行格式化输出，这是主要的格式化逻辑
        formatter = _get_node_formatter(current_node_type)
        if formatter:
            logger.debug(f"[LATS SSE] 使用节点专用格式化器: {current_node_type}")
            return formatter(message_type, raw_content)

        # 对于未知节点类型，使用默认格式化
        logger.debug(f"[LATS SSE] 使用默认格式化器处理未知节点: {current_node_type}")
        return _format_default_message(message_type, raw_content)

    except Exception as e:
        logger.error(f"[LATS SSE] 提取消息内容失败: {str(e)}")
        return ""


def _get_node_formatter(node_type: str):
    """根据节点类型获取对应的格式化函数"""
    formatters = {
        "generate_initial_response": _format_initial_response_message,
        "expand": _format_expand_message,
        "tools": _format_tool_message_by_node,
        "reflect": _format_reflect_message,
        "select": _format_select_message,
    }
    return formatters.get(node_type)


def _format_initial_response_message(message_type: str, content: str) -> str:
    """格式化初始响应节点的消息"""
    if "ToolMessage" in message_type:
        return "\n🔧 **初始信息收集完成**\n\n📊 已获取到基础信息，正在生成初始解决方案...\n\n"
    elif "AIMessage" in message_type:
        # 初始响应阶段的AI消息通常是第一个候选答案
        if _is_final_answer_content(content):
            return f"\n💡 **初始解决方案**\n\n{content}\n\n"
        elif len(content) > 30:
            return f"\n💡 **初始分析**\n\n{content}\n\n"
    return ""


def _format_expand_message(message_type: str, content: str) -> str:
    """格式化扩展搜索节点的消息"""
    if "ToolMessage" in message_type:
        return "\n🔧 **扩展搜索工具调用完成**\n\n📋 获取到新的信息，继续候选方案评估...\n\n"
    elif "AIMessage" in message_type:
        # 扩展阶段的消息按优先级处理
        if _is_evaluation_result(content):
            return "\n📊 **方案评估**\n\n🤔 正在分析多个解决方案的质量和可行性...\n\n"
        elif _is_final_answer_content(content):
            return f"\n\n🎯 **优化解决方案**\n\n{content}\n\n"
        elif len(content) > 50:
            return f"\n\n💡 **候选方案**\n\n{content}\n\n"
    return ""


def _format_tool_message_by_node(message_type: str, content: str) -> str:
    """基于节点的工具消息格式化"""
    if "ToolMessage" in message_type:
        if len(content) > 500:
            return "\n🔧 **工具执行完成**\n\n📊 已获取到详细信息，正在整理分析...\n\n"
        else:
            return "\n🔧 **工具执行完成**\n\n📋 已获取相关信息\n\n"
    elif "AIMessage" in message_type:
        # 工具节点的AI消息通常是对工具结果的处理
        if _is_final_answer_content(content):
            return f"\n\n🔧 **工具处理结果**\n\n{content}\n\n"
    return ""


def _format_reflect_message(message_type: str, content: str) -> str:
    """格式化反思节点的消息"""
    if "AIMessage" in message_type:
        if _is_evaluation_result(content):
            return "\n🤔 **方案反思与评估**\n\n📈 正在评估当前解决方案的质量...\n\n"
        elif len(content) > 30:
            return f"\n🤔 **反思分析**\n\n{content}\n\n"
    return ""


def _format_select_message(message_type: str, content: str) -> str:
    """格式化选择节点的消息"""
    if "AIMessage" in message_type:
        if _is_final_answer_content(content):
            return f"\n\n🎯 **最终选择**\n\n{content}\n\n"
        elif len(content) > 30:
            return f"\n🎯 **方案选择**\n\n{content}\n\n"
    return ""


def _format_default_message(message_type: str, content: str) -> str:
    """格式化未知节点类型的消息"""
    if "AIMessage" in message_type:
        if _is_final_answer_content(content):
            return f"\n\n📝 **答案内容**\n\n{content}\n\n"
        elif len(content) > 50:
            return f"\n\n� **回答**\n\n{content}\n\n"
    elif "ToolMessage" in message_type:
        return "\n🔧 **工具执行完成**\n\n📋 已获取信息\n\n"
    return ""


def _is_final_answer_content(content: str) -> bool:
    """判断是否是最终答案内容"""
    # 检查内容特征，避免内部信息泄露
    if _contains_internal_keywords(content):
        return False

    # 检查是否包含完整的回答结构
    answer_indicators = [
        "根据", "基于", "答案是", "解决方案", "总结", "建议",
        "因此", "所以", "综上", "最终", "结论", "介绍", "是",
        "包括", "具有", "特点", "功能", "用于", "支持", "提供",
        "参考资料", "如下", "以下", "主要", "可以", "能够",
        "数据库", "系统", "产品", "技术", "应用", "企业"
    ]

    # 如果内容包含回答指示词且长度合适，认为是最终答案
    has_indicators = any(
        indicator in content for indicator in answer_indicators)

    # 或者，如果内容较长且不包含内部关键词，也可能是最终答案
    is_substantial_content = len(
        content) > 50 and not _contains_internal_keywords(content)

    # 较宽松的判断：有指示词且不太短，或者是较长的实质内容
    return (has_indicators and len(content) > 15) or is_substantial_content


def _is_evaluation_result(content: str) -> bool:
    """判断是否是评估结果"""
    evaluation_keywords = [
        "评分", "score", "评估", "evaluation", "质量", "reflections",
        "found_solution", "解决方案", "候选"
    ]
    return any(keyword in content.lower() for keyword in evaluation_keywords)


def _contains_internal_keywords(content: str) -> bool:
    """检查是否包含内部关键词（更精确的版本）"""
    internal_keywords = [
        "以下是参考资料", "每份参考资料都由标题和内容组成", "以XML格式提供",
        "参考资料:", "<documents>", "</documents>", "基于上述参考资料",
        "根据参考资料", "参考以上信息", "System:", "Human:", "Assistant:",
        "以下是搜索结果", "搜索到的相关信息:", "知识库搜索结果:",
        "工具调用结果:", "Tool call result:", "Function call:",
        "根据工具执行结果", "基于搜索到的信息", "<title>", "</title>",
        "<content>", "</content>", "tool_call", "function_call",
        "usage_metadata", "response_metadata"
    ]

    content_lower = content.lower()
    return any(keyword.lower() in content_lower for keyword in internal_keywords)
