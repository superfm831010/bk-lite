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
        # 获取流式结果
        result = await workflow.stream(body)
        
        async for chunk in result:
            # 解析节点信息
            node_name = list(chunk.keys())[0] if chunk else None
            node_data = list(chunk.values())[0] if chunk else None
            
            logger.debug(f"处理节点: {node_name}, 数据类型: {type(node_data)}")
            
            # 处理不同类型的节点输出
            if node_name == "planner":
                await _handle_planner_node(formatter, res, node_data)
                plan_generated = True
                
            elif node_name == "agent":
                current_step_index += 1
                await _handle_agent_node(formatter, res, node_data, current_step_index)
                
            elif node_name == "replan":
                await _handle_replan_node(formatter, res, node_data)
                
            # 处理消息流
            if isinstance(node_data, dict) and "messages" in node_data:
                messages = node_data["messages"]
                if messages:
                    last_message = messages[-1]
                    
                    if isinstance(last_message, AIMessageChunk):
                        # 处理 AI 响应流
                        content = last_message.content
                        if content and content.strip():
                            await _handle_ai_content(formatter, res, content, node_name)
                    
                    elif isinstance(last_message, ToolMessage):
                        # 处理工具执行结果
                        await _handle_tool_message(formatter, res, last_message)
        
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
    await res.write(formatter.format_planning_start())
    
    # 提取计划步骤
    if isinstance(node_data, dict) and "plan" in node_data:
        plan_steps = node_data["plan"]
        if plan_steps:
            plan_chunk = formatter.format_plan_generated(plan_steps)
            await res.write(plan_chunk)


async def _handle_agent_node(formatter: PlanExecuteSSEFormatter, res, node_data: Dict[str, Any], step_index: int):
    """处理代理执行节点"""
    # 获取当前任务描述
    current_task = "执行计划步骤"
    if isinstance(node_data, dict) and "plan" in node_data and node_data["plan"]:
        plan = node_data["plan"]
        if step_index <= len(plan):
            current_task = plan[step_index - 1]
    
    step_start_chunk = formatter.format_step_start(step_index, current_task)
    await res.write(step_start_chunk)


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
    
    # 工具开始调用
    tool_start_chunk = formatter.format_tool_call_start(tool_name)
    await res.write(tool_start_chunk)
    
    # 工具执行结果
    result_summary = _summarize_tool_result(tool_content)
    tool_result_chunk = formatter.format_tool_result(tool_name, result_summary)
    await res.write(tool_result_chunk)


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
        lines = content.split('\n')
        steps = []
        
        for line in lines:
            line = line.strip()
            # 匹配编号的步骤
            if line and (line.startswith(('1.', '2.', '3.', '4.', '5.')) or 
                        line.startswith(('步骤1', '步骤2', '步骤3', '步骤4', '步骤5'))):
                # 清理步骤编号
                step = line.split('.', 1)[-1].strip() if '.' in line else line
                step = step.replace('步骤', '').strip()
                if step:
                    steps.append(step)
        
        return steps if steps else None
    except Exception as e:
        logger.warning(f"提取计划步骤失败: {str(e)}")
        return None
