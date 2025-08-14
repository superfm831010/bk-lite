"""
Plan and Execute Agent 优雅的 SSE 流式响应处理

提供类似 Claude 的优雅用户体验
"""
import uuid
import json as json_util
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from langchain_core.messages import AIMessageChunk, ToolMessage, AIMessage, HumanMessage
from sanic.log import logger

from src.api.agent.plan_execute_sse_formatter import PlanExecuteSSEFormatter, ExecutionPhase
from src.api.agent.sse_config import DEFAULT_SSE_CONFIG, SSEDisplayConfig


async def stream_plan_execute_response(workflow, body, res, config: SSEDisplayConfig = None):
    """
    改进的 Plan and Execute Agent SSE 流式响应处理
    
    Args:
        workflow: 工作流对象
        body: 请求体
        res: 响应对象
        config: SSE 显示配置
    """
    chat_id = str(uuid.uuid4())
    formatter = PlanExecuteSSEFormatter(chat_id, body.model, config or DEFAULT_SSE_CONFIG)
    
    # 用于跟踪状态
    current_step_index = 0
    plan_generated = False
    current_node = None
    accumulated_content = ""
    
    # 发送初始化状态
    init_chunk = formatter.format_initialization()
    await res.write(init_chunk)
    
    try:
        # 获取流式结果 - 使用 values 模式捕获状态变化
        graph = await workflow.compile_graph(body)
        config = workflow.get_config(body)
        
        # 直接使用图的 astream 方法，使用 values 模式来捕获所有状态变化
        result = graph.astream(body, config, stream_mode="values")
        
        async for chunk in result:
            # chunk 在 values 模式下是完整的状态快照
            logger.debug(f"处理状态快照: {type(chunk)}, 键: {list(chunk.keys()) if isinstance(chunk, dict) else 'N/A'}")
            
            # 检查状态变化
            if isinstance(chunk, dict):
                # 处理规划阶段
                if "plan" in chunk and chunk["plan"] and not plan_generated:
                    await _handle_plan_update(formatter, res, chunk)
                    plan_generated = True
                
                # 处理步骤执行
                current_step = chunk.get("current_step_index", 0)
                if current_step > current_step_index:
                    current_step_index = current_step
                    await _handle_step_progress(formatter, res, chunk, current_step_index)
                
                # 处理消息更新
                if "messages" in chunk and chunk["messages"]:
                    await _handle_message_updates(formatter, res, chunk["messages"])
        
        # 发送完成状态
        completion_chunk = formatter.format_completion()
        await res.write(completion_chunk)
        
    except Exception as e:
        logger.error(f"SSE 流处理错误: {str(e)}", exc_info=True)
        # 发送错误信息
        error_chunk = formatter.format_final_content(f"\n❌ **执行过程中出现错误：**{str(e)}\n")
        await res.write(error_chunk)
    
    finally:
        # 发送结束标记
        await res.write("data: [DONE]\n\n")


async def _handle_planner_node(formatter: PlanExecuteSSEFormatter, res, node_data: Dict[str, Any]):
    """处理规划节点"""
    logger.info("开始处理规划节点")
    await res.write(formatter.format_planning_start())
    
    # 提取计划步骤
    plan_steps = None
    
    if isinstance(node_data, dict):
        if "plan" in node_data:
            plan_steps = node_data["plan"]
            logger.info(f"从node_data中提取到计划: {plan_steps}")
        # 也检查是否在 messages 的最后一条消息中
        elif "messages" in node_data and node_data["messages"]:
            last_message = node_data["messages"][-1]
            if hasattr(last_message, 'content'):
                # 尝试从内容中提取计划
                plan_steps = _extract_plan_from_content(last_message.content)
                logger.info(f"从消息内容中提取到计划: {plan_steps}")
    
    if plan_steps:
        plan_chunk = formatter.format_plan_generated(plan_steps)
        await res.write(plan_chunk)
        logger.info("计划已发送到前端")
    else:
        logger.warning("未能从规划节点中提取计划步骤")
        # 发送一个占位的计划信息
        placeholder_chunk = formatter.format_final_content("📋 正在制定详细的执行计划...\n")
        await res.write(placeholder_chunk)


async def _handle_agent_node(formatter: PlanExecuteSSEFormatter, res, node_data: Dict[str, Any], step_index: int):
    """处理代理执行节点"""
    logger.info(f"开始处理代理节点，步骤索引: {step_index}")
    
    # 获取当前任务描述
    current_task = "执行计划步骤"
    if isinstance(node_data, dict) and "plan" in node_data and node_data["plan"]:
        plan = node_data["plan"]
        if step_index <= len(plan):
            current_task = plan[step_index - 1]
            logger.info(f"当前任务: {current_task}")
    
    step_start_chunk = formatter.format_step_start(step_index, current_task)
    await res.write(step_start_chunk)
    logger.info(f"步骤 {step_index} 开始信息已发送到前端")


async def _handle_plan_update(formatter: PlanExecuteSSEFormatter, res, state_chunk: Dict[str, Any]):
    """处理计划更新"""
    logger.info("处理计划更新")
    await res.write(formatter.format_planning_start())
    
    plan_steps = state_chunk.get("plan", [])
    if plan_steps:
        logger.info(f"发现计划步骤: {plan_steps}")
        plan_chunk = formatter.format_plan_generated(plan_steps)
        await res.write(plan_chunk)
    else:
        logger.warning("计划为空")


async def _handle_step_progress(formatter: PlanExecuteSSEFormatter, res, state_chunk: Dict[str, Any], step_index: int):
    """处理步骤进度更新"""
    logger.info(f"处理步骤进度更新: {step_index}")
    
    # 获取当前任务描述
    current_task = "执行计划步骤"
    plan = state_chunk.get("plan", [])
    if plan and step_index <= len(plan):
        current_task = plan[step_index - 1]
    
    step_start_chunk = formatter.format_step_start(step_index, current_task)
    await res.write(step_start_chunk)


async def _handle_message_updates(formatter: PlanExecuteSSEFormatter, res, messages: List):
    """处理消息更新"""
    logger.debug(f"处理消息更新，消息数量: {len(messages)}")
    
    # 处理最近的消息
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            # 处理工具执行结果
            await _handle_tool_message(formatter, res, message)
        
        elif isinstance(message, AIMessage):
            # 处理 AI 消息
            content = message.content
            if content and content.strip():
                # 检查是否包含工具调用
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    for tool_call in message.tool_calls:
                        tool_name = tool_call.get('name', '未知工具')
                        await _handle_tool_call_start(formatter, res, tool_name)
                else:
                    # 普通的 AI 内容
                    await _handle_ai_content(formatter, res, content, "agent")
        
        elif isinstance(message, AIMessageChunk):
            # 处理流式消息块
            content = message.content
            if content and content.strip():
                await _handle_ai_content(formatter, res, content, "agent")


async def _handle_tools_node(formatter: PlanExecuteSSEFormatter, res, node_data: Dict[str, Any]):
    """处理工具节点"""
    logger.debug(f"处理工具节点数据: {node_data}")
    # 工具节点通常包含工具执行的状态信息
    if isinstance(node_data, dict) and "messages" in node_data:
        messages = node_data["messages"]
        for message in messages:
            if isinstance(message, ToolMessage):
                await _handle_tool_message(formatter, res, message)


async def _handle_tool_call_start(formatter: PlanExecuteSSEFormatter, res, tool_name: str):
    """处理工具调用开始"""
    tool_start_chunk = formatter.format_tool_call_start(tool_name)
    await res.write(tool_start_chunk)


async def _handle_replan_node(formatter: PlanExecuteSSEFormatter, res, node_data: Dict[str, Any]):
    """处理重新规划节点"""
    reason = "需要调整执行策略"
    replan_chunk = formatter.format_replanning(reason)
    await res.write(replan_chunk)


async def _handle_ai_content(formatter: PlanExecuteSSEFormatter, res, content: str, node_name: str):
    """处理 AI 生成的内容"""
    # 判断是否是最终答案
    if node_name == "agent" and any(keyword in content.lower() for keyword in ["最终答案", "总结", "结论", "答案"]):
        # 开始最终答案生成
        final_start_chunk = formatter.format_final_answer_start()
        await res.write(final_start_chunk)
    
    # 流式输出内容
    if content.strip():
        content_chunk = formatter.format_final_content(content)
        await res.write(content_chunk)


async def _handle_tool_message(formatter: PlanExecuteSSEFormatter, res, tool_message: ToolMessage):
    """处理工具消息"""
    tool_name = getattr(tool_message, 'name', '未知工具')
    tool_content = tool_message.content
    
    logger.info(f"处理工具消息: {tool_name}")
    
    # 工具开始调用
    tool_start_chunk = formatter.format_tool_call_start(tool_name)
    await res.write(tool_start_chunk)
    
    # 工具执行结果
    result_summary = _summarize_tool_result(tool_content)
    tool_result_chunk = formatter.format_tool_result(tool_name, result_summary)
    await res.write(tool_result_chunk)
    
    logger.info(f"工具 {tool_name} 执行结果已发送到前端")


def _summarize_tool_result(content: str, max_length: int = 200) -> str:
    """总结工具执行结果"""
    if not content:
        return "执行完成"
    
    # 清理和截断内容
    content = content.strip()
    if len(content) <= max_length:
        return content
    
    # 尝试找到合适的截断点
    truncated = content[:max_length]
    
    # 在句号或换行符处截断
    for delimiter in ["。", ".\n", "\n", ". "]:
        last_delimiter = truncated.rfind(delimiter)
        if last_delimiter > max_length * 0.7:  # 确保不会截断太多
            return truncated[:last_delimiter + 1]
    
    return truncated + "..."


def _extract_plan_from_content(content: str) -> Optional[List[str]]:
    """从内容中提取计划步骤"""
    try:
        if not content or not isinstance(content, str):
            return None
            
        lines = content.split('\n')
        steps = []
        
        for line in lines:
            line = line.strip()
            # 匹配多种编号格式的步骤
            patterns = [
                r'^\d+\.\s*(.+)',  # 1. xxx
                r'^步骤\s*\d+[：:]\s*(.+)',  # 步骤1: xxx
                r'^第\s*\d+\s*步[：:]\s*(.+)',  # 第1步: xxx
                r'^-\s*(.+)',  # - xxx
                r'^\*\s*(.+)',  # * xxx
            ]
            
            import re
            for pattern in patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    step_content = match.group(1).strip()
                    if step_content and len(step_content) > 3:  # 过滤太短的内容
                        steps.append(step_content)
                    break
        
        # 如果没有找到结构化的步骤，尝试按句号分割
        if not steps and '。' in content:
            sentences = [s.strip() for s in content.split('。') if s.strip()]
            if len(sentences) >= 2 and len(sentences) <= 10:  # 合理的步骤数量
                steps = sentences[:5]  # 最多取前5个作为步骤
        
        return steps if steps else None
    except Exception as e:
        logger.warning(f"提取计划步骤失败: {str(e)}")
        return None
