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
    使用简化的标准SSE格式，提供优雅的用户体验
    """
    created = int(datetime.now().timestamp())
    sent_contents = set()  # 用于去重
    step_counter = 0  # 步骤计数器

    try:
        logger.info(f"[Plan Execute SSE] 开始流式处理，chat_id: {chat_id}")

        # 发送优雅的开始消息
        start_content = "🎯 **正在分析您的请求...**\n\n🔍 让我仔细理解您的需求\n\n📋 准备制定详细的执行计划\n\n"
        yield _create_sse_data(chat_id, created, model, start_content)
        sent_contents.add(start_content)
        await asyncio.sleep(0.2)

        # 获取流式迭代器
        stream_iter = await workflow.stream(body)

        async for chunk in stream_iter:
            logger.debug(f"[Plan Execute SSE] 收到 chunk: {type(chunk)}")

            # 增强的空值检查
            if not chunk or chunk is None:
                logger.debug(f"[Plan Execute SSE] 跳过空的或None的chunk")
                continue

            # chunk 是一个 tuple，包含消息对象
            if isinstance(chunk, (tuple, list)) and len(chunk) > 0:
                message = chunk[0]

                # 检查消息是否为None
                if message is None:
                    logger.debug(f"[Plan Execute SSE] 跳过None消息")
                    continue

                # 提取消息内容
                content = _extract_message_content(message, step_counter)

                if content and content not in sent_contents:
                    # 使用标准的OpenAI SSE格式
                    yield _create_sse_data(chat_id, created, model, content)
                    sent_contents.add(content)
                    logger.info(f"[Plan Execute SSE] 发送内容: {content[:50]}...")

                    # 根据内容类型调整延迟
                    if "**执行步骤" in content:
                        step_counter += 1
                        await asyncio.sleep(0.3)  # 步骤开始时稍微长一点的延迟
                    elif "工具执行完成" in content:
                        await asyncio.sleep(0.2)  # 工具完成时适当延迟
                    else:
                        await asyncio.sleep(0.1)  # 其他内容较短延迟

        # 发送优雅的完成消息
        completion_content = "\n\n---\n\n✨ **任务执行完成！**\n\n🎉 所有步骤都已成功完成\n\n💫 希望我的回答对您有帮助"
        yield _create_sse_data(chat_id, created, model, completion_content)

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
        yield f"data: {json_str}\n\n"

        logger.info(f"[Plan Execute SSE] 流式处理完成，chat_id: {chat_id}")

    except Exception as e:
        logger.error(f"[Plan Execute SSE] 处理过程中出错: {str(e)}", exc_info=True)
        # 发送优雅的错误消息
        error_content = f"\n\n---\n\n❌ **处理过程中遇到了一些问题**\n\n🔧 **错误详情：**\n{str(e)}\n\n💡 **建议：**\n请稍后重试，或联系技术支持获取帮助"
        yield _create_sse_data(chat_id, created, model, error_content, finish_reason="stop")


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


def _extract_message_content(message: Any, step_counter: int = 0) -> str:
    """
    从消息对象中提取内容，优化显示效果
    """
    content = ""

    try:
        # 首先检查消息是否为None
        if message is None:
            logger.debug(f"[Plan Execute SSE] 消息为None，跳过处理")
            return ""

        message_type = type(message).__name__
        logger.debug(f"[Plan Execute SSE] 处理消息类型: {message_type}")

        # 检查消息是否有content属性
        if hasattr(message, 'content'):
            raw_content = message.content
            logger.debug(f"[Plan Execute SSE] 消息内容: {raw_content}")

            if isinstance(raw_content, str) and raw_content.strip():
                content = raw_content.strip()

                # 优化显示逻辑
                if "ToolMessage" in message_type:
                    # 工具结果通常很长，需要格式化
                    content = _format_tool_result(content)
                elif "AIMessage" in message_type:
                    # AI消息需要过滤和美化
                    content = _format_ai_message(content, step_counter)
                elif "SystemMessage" in message_type:
                    # 跳过系统消息
                    return ""
                elif "HumanMessage" in message_type:
                    # 用户消息通常是内部流程，可能需要过滤
                    if _is_internal_process_message(content):
                        return ""
                    content = f"🤔 **思考中...**\n\n{content}"
                else:
                    content = _format_general_message(content)

        # 检查消息是否有其他可能的内容字段
        elif hasattr(message, 'text'):
            content = message.text.strip() if message.text else ""
        elif hasattr(message, 'data'):
            content = str(message.data).strip() if message.data else ""

        return content

    except Exception as e:
        logger.error(f"[Plan Execute SSE] 提取消息内容失败: {str(e)}")
        return ""


def _format_tool_result(content: str) -> str:
    """格式化工具执行结果"""
    # 如果是很长的结果，只显示摘要
    if len(content) > 500:
        return f"\n🔧 **工具执行完成**\n\n📊 已获取到详细信息，正在整理分析...\n\n⚡ 继续执行下一步"
    else:
        return f"\n🔧 **工具执行完成**\n\n📋 结果：{content}\n\n"


def _format_ai_message(content: str, step_counter: int = 0) -> str:
    """格式化AI消息，提取关键信息"""
    try:
        # 尝试解析JSON格式的计划
        if content.startswith('{"steps"'):
            import json
            data = json.loads(content)
            if "steps" in data:
                steps = data["steps"]
                formatted_steps = []
                for i, step in enumerate(steps):
                    formatted_steps.append(f"   **{i+1}.** {step}")
                steps_text = "\n\n".join(formatted_steps)
                return f"\n\n📋 **执行计划已制定**\n\n🎯 **总共 {len(steps)} 个步骤：**\n\n{steps_text}\n\n🚀 **开始执行任务**\n\n"

        # 尝试解析action格式
        elif content.startswith('{"action"'):
            # 这通常是最终结果，格式化输出
            import json
            data = json.loads(content)
            if "action" in data and "response" in data["action"]:
                response = data["action"]["response"]
                return f"\n\n---\n\n✨ **最终答案**\n\n{response}\n\n"

        # 其他AI消息的优雅格式化
        elif "步骤" in content or "计划" in content:
            return f"\n📋 **制定计划中...**\n\n{content}\n\n"
        elif "最终答案" in content or "任务完成" in content:
            return f"\n✅ **任务即将完成**\n\n{content}\n\n"
        elif "执行步骤" in content or content.strip().startswith("步骤"):
            return f"\n⚡ **执行步骤 {step_counter + 1}**\n\n{content}\n\n"
        else:
            # 为普通内容添加适当的间距和emoji
            if len(content) > 100:
                return f"\n🤖 **处理中...**\n\n{content}\n\n"
            else:
                return f"\n💭 {content}\n\n"

    except Exception as e:
        logger.debug(f"JSON解析失败: {e}")
        # JSON解析失败，进行智能格式化
        if "工具" in content:
            return f"\n🔧 **工具调用**\n\n{content}\n\n"
        elif "搜索" in content:
            return f"\n🔍 **信息搜索**\n\n{content}\n\n"
        elif "分析" in content:
            return f"\n📊 **数据分析**\n\n{content}\n\n"
        else:
            return f"\n🤖 {content}\n\n"


def _format_general_message(content: str) -> str:
    """格式化一般消息"""
    if "执行步骤" in content:
        return f"\n⚡ **执行中...**\n\n{content}\n\n"
    elif "完成" in content:
        return f"\n✅ **完成**\n\n{content}\n\n"
    elif "搜索" in content:
        return f"\n🔍 **搜索中...**\n\n{content}\n\n"
    elif "分析" in content:
        return f"\n📊 **分析中...**\n\n{content}\n\n"
    else:
        return f"\n📝 {content}\n\n"


def _is_internal_process_message(content: str) -> bool:
    """判断是否是内部流程消息，需要过滤"""
    internal_patterns = [
        "You are tasked with executing step",
        "For the following plan:",
        "已完成的步骤:",
        "如果这是最后一个步骤",
        "所有计划步骤已完成",
        "请根据以下执行结果综合给出最终答案",
        "重要说明：",
        "请直接提供最终的答案"
    ]

    for pattern in internal_patterns:
        if pattern in content:
            return True
    return False


def _extract_meaningful_content(node_name: str, node_data: Any) -> str:
    """
    提取有意义的内容，尽量保留更多信息
    """
    content = ""

    try:
        logger.debug(
            f"[Plan Execute SSE] 处理节点 {node_name}, 数据类型: {type(node_data)}")

        if isinstance(node_data, dict):
            # 从messages中提取内容
            if "messages" in node_data and isinstance(node_data["messages"], list):
                for message in node_data["messages"]:
                    if isinstance(message, dict):
                        msg_content = message.get("content", "")
                        if isinstance(msg_content, str) and msg_content.strip():
                            # 只过滤明显的技术内容
                            if not _is_obvious_technical_message(msg_content):
                                content = msg_content.strip()
                                logger.debug(
                                    f"[Plan Execute SSE] 从messages提取内容: {content[:50]}...")
                                break

            # 直接提取内容字段
            elif "content" in node_data:
                msg_content = node_data["content"]
                if isinstance(msg_content, str) and msg_content.strip():
                    if not _is_obvious_technical_message(msg_content):
                        content = msg_content.strip()
                        logger.debug(
                            f"[Plan Execute SSE] 从content字段提取内容: {content[:50]}...")

        elif isinstance(node_data, str) and node_data.strip():
            if not _is_obvious_technical_message(node_data):
                content = node_data.strip()
                logger.debug(
                    f"[Plan Execute SSE] 直接提取字符串内容: {content[:50]}...")

        # 为不同节点添加适当的前缀和格式
        if content:
            if node_name == "llm":
                content = f"\n📋 **制定计划**\n\n{content}\n\n"
            elif node_name == "act":
                content = f"\n⚡ **执行任务**\n\n{content}\n\n"
            elif node_name == "replan":
                content = f"\n🔄 **重新规划**\n\n💡 需要调整策略\n\n{content}\n\n"
            else:
                content = f"\n🔸 **{node_name}**\n\n{content}\n\n"

        return content

    except Exception as e:
        logger.error(f"[Plan Execute SSE] 提取内容失败: {str(e)}")
        return ""


def _is_obvious_technical_message(content: str) -> bool:
    """
    判断是否是明显的技术性消息，减少过滤条件
    """
    if not content or len(content.strip()) < 3:
        return True

    # 只过滤最明显的技术内容
    obvious_technical_patterns = [
        "tool_call_id:",
        "function_call:",
        "usage_metadata:",
        "response_metadata:",
        '"type":"function"',
        '"role":"function"',
        '{"id":"',
        '{"object":"',
        "uuid-"
    ]

    content_lower = content.lower()

    # 检查是否包含明显的技术模式
    for pattern in obvious_technical_patterns:
        if pattern in content_lower:
            logger.debug(f"[Plan Execute SSE] 过滤技术内容: {pattern}")
            return True

    # 过滤纯JSON格式但长度较短的内容
    if (content.strip().startswith('{') and content.strip().endswith('}') and
            len(content.strip()) < 50):
        try:
            json.loads(content)
            logger.debug(f"[Plan Execute SSE] 过滤短JSON内容")
            return True
        except:
            pass

    return False
