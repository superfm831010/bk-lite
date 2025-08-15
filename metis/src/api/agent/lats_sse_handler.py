"""
LATS Agent SSE 处理器

负责处理 LATS Agent 的流式输出，将搜索过程转换为优雅的 SSE 响应
"""
import asyncio
import json
import re
from typing import Dict, Any, AsyncGenerator, List
from datetime import datetime

from sanic.log import logger
from src.api.agent.lats_sse_formatter import LatsSSEFormatter


async def stream_lats_response(
    workflow,
    body: Dict[str, Any],
    chat_id: str,
    model: str,
    res
):
    """
    流式处理 LATS Agent 响应
    提供优雅的树搜索过程可视化

    Args:
        workflow: LATS工作流实例
        body: 请求体
        chat_id: 聊天ID  
        model: 模型名称
        res: Sanic ResponseStream 对象
    """
    created = int(datetime.now().timestamp())
    formatter = LatsSSEFormatter(chat_id, model)
    sent_contents = set()  # 用于去重

    # 搜索状态跟踪
    search_stats = {
        "iteration": 0,
        "tree_height": 0,
        "nodes_explored": 0,
        "best_score": 0.0,
        "solution_found": False,
        "in_tool_call": False,
        "current_tool": None
    }

    try:
        logger.info(f"[LATS SSE] 开始流式处理，chat_id: {chat_id}")

        # 发送初始化消息
        init_content = formatter.format_initialization()
        await res.write(init_content)
        await asyncio.sleep(0.3)

        # 获取流式迭代器
        stream_iter = await workflow.stream(body)

        # 跟踪当前处理阶段
        current_phase = "init"
        tool_calls_buffer = []
        candidate_evaluations = []

        async for chunk in stream_iter:
            logger.debug(f"[LATS SSE] 收到 chunk: {type(chunk)}")

            if not chunk or chunk is None:
                logger.debug(f"[LATS SSE] 跳过空的或None的chunk")
                continue

            # chunk 是一个 tuple，包含消息对象
            if isinstance(chunk, (tuple, list)) and len(chunk) > 0:
                message = chunk[0]

                if message is None:
                    logger.debug(f"[LATS SSE] 跳过None消息")
                    continue

                # 分析消息内容，确定当前阶段
                content = _extract_message_content(message)
                if not content:
                    continue

                # 智能识别搜索阶段并生成相应的 SSE 内容
                sse_content = await _process_lats_message(
                    content, message, formatter, search_stats, current_phase
                )

                if sse_content and sse_content not in sent_contents:
                    await res.write(sse_content)
                    sent_contents.add(sse_content)
                    logger.debug(
                        f"[LATS SSE] 发送内容: {_extract_content_preview(sse_content)}")

                    # 根据内容类型调整延迟
                    if "搜索迭代" in sse_content:
                        await asyncio.sleep(0.4)
                    elif "评估" in sse_content:
                        await asyncio.sleep(0.3)
                    elif "工具" in sse_content:
                        await asyncio.sleep(0.2)
                    else:
                        await asyncio.sleep(0.1)

        # 发送完成消息
        completion_content = formatter.format_completion(search_stats)
        await res.write(completion_content)

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
        await res.write(f"data: {json_str}\n\n")
        await res.write("data: [DONE]\n\n")

        logger.info(f"[LATS SSE] 流式处理完成，chat_id: {chat_id}")

    except Exception as e:
        logger.error(f"[LATS SSE] 处理过程中出错: {str(e)}", exc_info=True)
        # 发送优雅的错误消息
        error_content = f"\n\n---\n\n❌ **LATS 搜索过程中遇到问题**\n\n🔧 **错误详情：**\n{str(e)}\n\n💡 **建议：**\n请稍后重试，或联系技术支持获取帮助"
        error_sse = _create_sse_data(
            chat_id, created, model, error_content, finish_reason="stop")
        await res.write(error_sse)


async def _process_lats_message(
    content: str,
    message: Any,
    formatter: LatsSSEFormatter,
    search_stats: Dict[str, Any],
    current_phase: str
) -> str:
    """
    处理 LATS 消息，返回格式化的 SSE 内容
    """
    try:
        message_type = type(message).__name__

        # 检测和处理初始响应生成
        if _is_initial_generation_message(content):
            return formatter.format_initial_generation_start()

        # 检测工具调用
        if "ToolMessage" in message_type or _is_tool_call_message(content):
            if not search_stats["in_tool_call"]:
                search_stats["in_tool_call"] = True
                tool_name = _extract_tool_name(content, message)
                if tool_name:
                    search_stats["current_tool"] = tool_name
                    return formatter.format_tool_call_start(tool_name)
            else:
                # 工具调用结果
                search_stats["in_tool_call"] = False
                tool_name = search_stats.get("current_tool", "工具")
                return formatter.format_tool_result(tool_name, content[:200])

        # 检测初始评估结果
        initial_eval = _extract_initial_evaluation(content)
        if initial_eval:
            search_stats["best_score"] = initial_eval["score"]
            return formatter.format_initial_evaluation(
                initial_eval["score"],
                initial_eval["reflection"],
                initial_eval.get("solution_preview")
            )

        # 检测搜索迭代
        iteration_info = _extract_iteration_info(content)
        if iteration_info:
            search_stats.update(iteration_info)
            return formatter.format_tree_search_iteration_start(
                iteration_info["iteration"],
                iteration_info["tree_height"],
                iteration_info["nodes_explored"]
            )

        # 检测候选生成
        if _is_candidate_generation_message(content):
            return formatter.format_candidates_generation_start()

        # 检测候选评估
        evaluation_results = _extract_evaluation_results(content)
        if evaluation_results:
            search_stats["best_score"] = max(search_stats["best_score"],
                                             evaluation_results.get("best_score", 0))
            return formatter.format_candidates_evaluation_results(
                evaluation_results["evaluations"]
            )

        # 检测解决方案发现
        solution_info = _extract_solution_found(content)
        if solution_info:
            search_stats["solution_found"] = True
            search_stats["best_score"] = solution_info["score"]
            return formatter.format_solution_found(
                solution_info["score"],
                solution_info["preview"],
                search_stats
            )

        # 检测搜索深度限制
        if _is_depth_limit_message(content):
            return formatter.format_search_depth_limit(5)  # MAX_TREE_HEIGHT

        # 检测最终答案生成
        if _is_final_answer_message(content):
            return formatter.format_final_answer_start()

        # 处理最终内容输出
        if _is_final_content(content, message_type):
            return formatter.format_final_content(content)

        # 其他消息的默认处理
        return _format_generic_message(content, formatter)

    except Exception as e:
        logger.error(f"[LATS SSE] 处理消息失败: {str(e)}")
        return ""


def _extract_message_content(message: Any) -> str:
    """从消息对象中提取内容"""
    try:
        if message is None:
            return ""

        if hasattr(message, 'content') and message.content:
            return message.content.strip()
        elif hasattr(message, 'text') and message.text:
            return message.text.strip()
        elif hasattr(message, 'data') and message.data:
            return str(message.data).strip()

        return ""
    except Exception as e:
        logger.error(f"[LATS SSE] 提取消息内容失败: {str(e)}")
        return ""


def _is_initial_generation_message(content: str) -> bool:
    """检测是否是初始生成消息"""
    patterns = [
        "开始生成初始响应",
        "生成初始回答",
        "初始回答生成完成",
        "GenerateInitialCandidate"
    ]
    return any(pattern in content for pattern in patterns)


def _is_tool_call_message(content: str) -> bool:
    """检测是否是工具调用相关消息"""
    patterns = [
        "tool_call",
        "工具调用",
        "执行工具",
        "调用工具",
        "tool_name"
    ]
    return any(pattern in content for pattern in patterns)


def _extract_tool_name(content: str, message: Any) -> str:
    """提取工具名称"""
    try:
        # 从消息属性中提取
        if hasattr(message, 'name') and message.name:
            return message.name

        # 从内容中提取
        if "tool_name" in content:
            match = re.search(r"tool_name[\"']?\s*:\s*[\"']?(\w+)", content)
            if match:
                return match.group(1)

        # 从中文描述中提取
        tool_patterns = [
            r"调用工具[：:]\s*(\w+)",
            r"执行工具[：:]\s*(\w+)",
            r"使用\s*(\w+)\s*工具"
        ]

        for pattern in tool_patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)

        return "工具"
    except Exception:
        return "工具"


def _extract_initial_evaluation(content: str) -> Dict[str, Any]:
    """提取初始评估信息"""
    try:
        # 查找评分信息
        score_patterns = [
            r"评分[：:]\s*(\d+(?:\.\d+)?)",
            r"分数[：:]\s*(\d+(?:\.\d+)?)",
            r"score[\"']?\s*:\s*(\d+(?:\.\d+)?)"
        ]

        score = None
        for pattern in score_patterns:
            match = re.search(pattern, content)
            if match:
                score = float(match.group(1))
                break

        if score is None:
            return None

        # 提取反思内容
        reflection_patterns = [
            r"反思[：:](.+?)(?:\n|$)",
            r"评估[：:](.+?)(?:\n|$)",
            r"reflections[\"']?\s*:\s*[\"'](.+?)[\"']"
        ]

        reflection = ""
        for pattern in reflection_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                reflection = match.group(1).strip()
                break

        return {
            "score": score,
            "reflection": reflection,
            "solution_preview": content[:200] if len(content) > 200 else content
        }

    except Exception as e:
        logger.debug(f"[LATS SSE] 提取初始评估失败: {str(e)}")
        return None


def _extract_iteration_info(content: str) -> Dict[str, Any]:
    """提取搜索迭代信息"""
    try:
        iteration_patterns = [
            r"搜索迭代\s*#?(\d+)",
            r"迭代\s*#?(\d+)",
            r"iteration\s*:?\s*(\d+)"
        ]

        height_patterns = [
            r"树高度[：:]\s*(\d+)",
            r"高度[：:]\s*(\d+)",
            r"height[：:]\s*(\d+)"
        ]

        nodes_patterns = [
            r"已探索[：:]\s*(\d+)",
            r"节点数[：:]\s*(\d+)",
            r"nodes_explored[：:]\s*(\d+)"
        ]

        iteration = None
        tree_height = 0
        nodes_explored = 0

        for pattern in iteration_patterns:
            match = re.search(pattern, content)
            if match:
                iteration = int(match.group(1))
                break

        for pattern in height_patterns:
            match = re.search(pattern, content)
            if match:
                tree_height = int(match.group(1))
                break

        for pattern in nodes_patterns:
            match = re.search(pattern, content)
            if match:
                nodes_explored = int(match.group(1))
                break

        if iteration is not None:
            return {
                "iteration": iteration,
                "tree_height": tree_height,
                "nodes_explored": nodes_explored
            }

        return None

    except Exception as e:
        logger.debug(f"[LATS SSE] 提取迭代信息失败: {str(e)}")
        return None


def _is_candidate_generation_message(content: str) -> bool:
    """检测是否是候选生成消息"""
    patterns = [
        "生成.*候选",
        "候选解决方案",
        "generate.*candidate",
        "新候选",
        "候选方案"
    ]
    return any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)


def _extract_evaluation_results(content: str) -> Dict[str, Any]:
    """提取评估结果信息"""
    try:
        # 查找评估结果汇总的模式
        if "评估结果汇总" in content or "candidate.*evaluation" in content.lower():

            # 提取最高评分
            best_score = 0
            score_patterns = [
                r"最高评分[：:]\s*(\d+(?:\.\d+)?)",
                r"最佳[：:]\s*(\d+(?:\.\d+)?)",
                r"max.*score[：:]\s*(\d+(?:\.\d+)?)"
            ]

            for pattern in score_patterns:
                match = re.search(pattern, content)
                if match:
                    best_score = float(match.group(1))
                    break

            # 提取解决方案数量
            solutions_count = 0
            solution_patterns = [
                r"找到\s*(\d+)\s*个解决方案",
                r"(\d+)\s*个解决方案",
                r"solutions[：:]\s*(\d+)"
            ]

            for pattern in solution_patterns:
                match = re.search(pattern, content)
                if match:
                    solutions_count = int(match.group(1))
                    break

            # 构建评估列表（简化版）
            evaluations = []
            for i in range(min(5, 3)):  # 最多3个候选
                evaluations.append({
                    "score": best_score - i * 0.5,
                    "found_solution": i < solutions_count
                })

            return {
                "best_score": best_score,
                "evaluations": evaluations
            }

        return None

    except Exception as e:
        logger.debug(f"[LATS SSE] 提取评估结果失败: {str(e)}")
        return None


def _extract_solution_found(content: str) -> Dict[str, Any]:
    """提取解决方案发现信息"""
    try:
        solution_patterns = [
            r"找到.*解决方案",
            r"solution.*found",
            r"高质量解决方案",
            r"最佳解决方案"
        ]

        for pattern in solution_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                # 提取评分
                score_match = re.search(r"评分[：:]\s*(\d+(?:\.\d+)?)", content)
                score = float(score_match.group(1)) if score_match else 9.0

                return {
                    "score": score,
                    "preview": content[:300]
                }

        return None

    except Exception as e:
        logger.debug(f"[LATS SSE] 提取解决方案信息失败: {str(e)}")
        return None


def _is_depth_limit_message(content: str) -> bool:
    """检测是否达到搜索深度限制"""
    patterns = [
        "搜索深度达到上限",
        "深度.*限制",
        "MAX_TREE_HEIGHT",
        "搜索深度超过"
    ]
    return any(pattern in content for pattern in patterns)


def _is_final_answer_message(content: str) -> bool:
    """检测是否是最终答案生成消息"""
    patterns = [
        "整理最终答案",
        "生成最终答案",
        "final.*answer",
        "最终回答",
        "综合.*答案"
    ]
    return any(pattern in content for pattern in patterns)


def _is_final_content(content: str, message_type: str) -> bool:
    """检测是否是最终内容"""
    # 如果是AI消息且包含实质性内容，且不是内部处理消息
    if "AIMessage" in message_type and len(content) > 50:
        internal_patterns = [
            "候选解决方案",
            "评估结果",
            "搜索迭代",
            "工具调用",
            "reflection",
            "score"
        ]

        # 如果不包含内部处理关键词，可能是最终内容
        is_internal = any(pattern in content for pattern in internal_patterns)
        return not is_internal

    return False


def _format_generic_message(content: str, formatter: LatsSSEFormatter) -> str:
    """格式化通用消息"""
    # 根据内容特征进行简单格式化
    if "搜索" in content:
        return f"\n🔍 **搜索进展**\n\n{content[:200]}...\n"
    elif "分析" in content:
        return f"\n📊 **分析中**\n\n{content[:200]}...\n"
    elif "评估" in content:
        return f"\n📋 **评估进展**\n\n{content[:200]}...\n"
    else:
        return f"\n💭 {content[:200]}...\n"


def _extract_content_preview(sse_content: str) -> str:
    """提取SSE内容的预览"""
    try:
        # 尝试解析JSON
        if "data: " in sse_content:
            json_part = sse_content.replace("data: ", "").strip()
            data = json.loads(json_part)
            if "choices" in data and data["choices"]:
                delta = data["choices"][0].get("delta", {})
                content = delta.get("content", "")
                return content[:50] + "..." if len(content) > 50 else content
        return sse_content[:50]
    except:
        return sse_content[:50]


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
