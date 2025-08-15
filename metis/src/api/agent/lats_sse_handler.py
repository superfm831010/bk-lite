"""
LATS Agent SSE 处理器

简化版实现，参考 Plan and Execute Agent 的成功模式
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
    使用简化的标准SSE格式，提供优雅的用户体验
    """
    created = int(datetime.now().timestamp())
    sent_contents = set()  # 用于去重
    iteration_counter = 0  # 迭代计数器

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
            logger.debug(f"[LATS SSE] 收到 chunk: {type(chunk)}")

            # 增强的空值检查
            if not chunk or chunk is None:
                logger.debug(f"[LATS SSE] 跳过空的或None的chunk")
                continue

            # chunk 是一个 tuple，包含消息对象
            if isinstance(chunk, (tuple, list)) and len(chunk) > 0:
                message = chunk[0]

                # 检查消息是否为None
                if message is None:
                    logger.debug(f"[LATS SSE] 跳过None消息")
                    continue

                # 提取消息内容
                content = _extract_message_content(message, iteration_counter)

                if content and content not in sent_contents:
                    # 使用标准的OpenAI SSE格式
                    await res.write(_create_sse_data(chat_id, created, model, content).encode('utf-8'))
                    sent_contents.add(content)
                    logger.info(f"[LATS SSE] 发送内容: {content[:50]}...")

                    # 根据内容类型调整延迟
                    if "搜索迭代" in content or "候选解决方案" in content:
                        iteration_counter += 1
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


def _extract_message_content(message: Any, iteration_counter: int = 0) -> str:
    """
    从消息对象中提取内容，优化显示效果
    """
    content = ""

    try:
        # 首先检查消息是否为None
        if message is None:
            logger.debug(f"[LATS SSE] 消息为None，跳过处理")
            return ""

        message_type = type(message).__name__
        logger.debug(f"[LATS SSE] 处理消息类型: {message_type}")

        # 检查消息是否有content属性
        if hasattr(message, 'content'):
            raw_content = message.content
            logger.debug(f"[LATS SSE] 消息内容: {raw_content}")

            if isinstance(raw_content, str) and raw_content.strip():
                content = raw_content.strip()

                # 优化显示逻辑 - 根据消息类型和内容特征
                if "ToolMessage" in message_type:
                    # 工具结果通常很长，需要格式化
                    content = _format_tool_result(content)
                elif "AIMessage" in message_type:
                    # AI消息需要过滤和美化
                    content = _format_ai_message(content, iteration_counter)
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
        logger.error(f"[LATS SSE] 提取消息内容失败: {str(e)}")
        return ""


def _format_tool_result(content: str) -> str:
    """格式化工具执行结果"""
    # 如果是很长的结果，只显示摘要
    if len(content) > 500:
        return f"\n🔧 **工具执行完成**\n\n📊 已获取到详细信息，正在整理分析...\n\n⚡ 继续执行下一步"
    else:
        return f"\n🔧 **工具执行完成**\n\n📋 结果：{content}\n\n"


def _format_ai_message(content: str, iteration_counter: int = 0) -> str:
    """格式化AI消息，提取关键信息"""
    try:
        # 检测 LATS 特定的消息模式

        # 1. 初始响应评估
        if "初始响应评估结果" in content or "initial.*evaluation" in content.lower():
            return _format_initial_evaluation(content)

        # 2. 搜索迭代信息
        if "搜索迭代" in content or "iteration" in content.lower():
            return _format_search_iteration(content, iteration_counter)

        # 3. 候选解决方案评估
        if "候选解决方案" in content or "candidate.*evaluation" in content.lower():
            return _format_candidate_evaluation(content)

        # 4. 解决方案发现
        if "找到.*解决方案" in content or "solution.*found" in content.lower():
            return _format_solution_found(content)

        # 5. 尝试解析JSON格式的内容
        if content.startswith('{') and content.endswith('}'):
            try:
                import json
                data = json.loads(content)

                # 检查是否是评估结果
                if "score" in data and "reflections" in data:
                    score = data.get("score", 0)
                    reflections = data.get("reflections", "")
                    return f"\n📊 **方案评估**\n\n⭐ 评分：**{score}/10**\n💭 评估：{reflections[:150]}...\n\n"

                # 检查是否是候选解决方案
                if "steps" in data or "candidates" in data:
                    return f"\n🧬 **生成候选方案**\n\n💡 正在创建多个解决方案候选...\n\n"

            except:
                pass

        # 6. 长文本内容可能是最终答案
        if len(content) > 200 and not _contains_technical_keywords(content):
            return f"\n\n📝 **答案内容**\n\n{content}\n\n"

        # 7. 其他有意义的内容
        if len(content) > 50:
            return f"\n💭 **处理中**\n\n{content[:200]}...\n\n"

        # 短内容可能是调试信息，跳过
        return ""

    except Exception as e:
        logger.debug(f"AI消息格式化失败: {e}")
        # 默认格式化
        if len(content) > 100:
            return f"\n🤖 **处理中...**\n\n{content}\n\n"
        else:
            return ""


def _format_initial_evaluation(content: str) -> str:
    """格式化初始评估结果"""
    # 提取评分
    score_match = re.search(r"评分[：:]\s*(\d+(?:\.\d+)?)", content)
    score = score_match.group(1) if score_match else "未知"

    return f"\n📊 **初始方案评估完成**\n\n⭐ 评分：**{score}/10**\n\n🚀 开始树搜索优化...\n\n"


def _format_search_iteration(content: str, iteration: int) -> str:
    """格式化搜索迭代"""
    return f"\n\n---\n\n🌳 **搜索迭代 #{iteration + 1}**\n\n🔍 正在探索搜索树的新分支...\n\n"


def _format_candidate_evaluation(content: str) -> str:
    """格式化候选评估"""
    return f"\n📈 **候选方案评估中**\n\n🤔 分析多个候选解决方案的质量...\n\n"


def _format_solution_found(content: str) -> str:
    """格式化解决方案发现"""
    return f"\n\n🎉 **找到高质量解决方案！**\n\n✨ 正在整理最终答案...\n\n"


def _format_general_message(content: str) -> str:
    """格式化一般消息"""
    if "搜索" in content:
        return f"\n🔍 **搜索进展**\n\n{content}\n\n"
    elif "分析" in content:
        return f"\n📊 **分析中**\n\n{content}\n\n"
    elif "评估" in content:
        return f"\n📋 **评估进展**\n\n{content}\n\n"
    else:
        return f"\n📝 {content}\n\n"


def _contains_technical_keywords(content: str) -> bool:
    """检查是否包含技术关键词"""
    technical_keywords = [
        "tool_call", "function", "usage_metadata", "response_metadata",
        "token", "prompt", "completion", "uuid", "reflection", "score:",
        "found_solution", "candidate", "iteration"
    ]

    content_lower = content.lower()
    return any(keyword in content_lower for keyword in technical_keywords)


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
