"""
Plan and Execute Agent SSE 格式化器

负责将 Plan and Execute Agent 的执行过程格式化为优雅的 SSE 输出，
提供类似 Claude 的用户体验
"""
import json
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

from src.web.api.agent.plan_and_execute_agent.sse_config import SSEDisplayConfig, DEFAULT_SSE_CONFIG


class ExecutionPhase(Enum):
    """执行阶段枚举"""
    INITIALIZING = "initializing"  # 初始化
    PLANNING = "planning"          # 规划中
    EXECUTING = "executing"        # 执行中
    REPLANNING = "replanning"      # 重新规划
    TOOL_CALLING = "tool_calling"  # 工具调用
    FINALIZING = "finalizing"      # 最终化
    COMPLETED = "completed"        # 已完成


@dataclass
class ExecutionStatus:
    """执行状态"""
    phase: ExecutionPhase
    step_index: int = 0
    total_steps: int = 0
    current_task: str = ""
    tool_name: str = ""
    progress_percentage: int = 0


class PlanExecuteSSEFormatter:
    """Plan and Execute Agent SSE 格式化器"""
    
    def __init__(self, chat_id: str, model: str, config: SSEDisplayConfig = None):
        self.chat_id = chat_id
        self.model = model
        self.config = config or DEFAULT_SSE_CONFIG
        self.created_time = int(datetime.now().timestamp())
        self.current_status = ExecutionStatus(ExecutionPhase.INITIALIZING)
        self.plan_steps: List[str] = []
        self.completed_steps: List[str] = []
        self.start_time = datetime.now()
        
    def _create_base_response(self, delta_content: str = None, 
                            finish_reason: str = None,
                            metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """创建基础响应对象"""
        response = {
            "id": self.chat_id,
            "object": "chat.completion.chunk",
            "created": self.created_time,
            "model": self.model,
            "choices": [{
                "delta": {"role": "assistant"},
                "index": 0,
                "finish_reason": finish_reason
            }],
            # 添加自定义元数据用于前端渲染
            "metis_metadata": {
                "execution_phase": self.current_status.phase.value,
                "step_index": self.current_status.step_index,
                "total_steps": self.current_status.total_steps,
                "progress_percentage": self.current_status.progress_percentage,
                **(metadata or {})
            }
        }
        
        if delta_content is not None:
            response["choices"][0]["delta"]["content"] = delta_content
            
        return response
    
    def _format_sse_data(self, response: Dict[str, Any]) -> str:
        """格式化 SSE 数据，确保中文字符正确编码"""
        json_str = json.dumps(response, ensure_ascii=False, separators=(',', ':'))
        return f"data: {json_str}\n\n"
    
    def format_initialization(self) -> str:
        """格式化初始化阶段"""
        self.current_status.phase = ExecutionPhase.INITIALIZING
        content = self.config.phase_texts.get("initializing", "分析问题中...")
        
        response = self._create_base_response(
            delta_content=content,
            metadata={"status_message": "初始化中"}
        )
        return self._format_sse_data(response)
    
    def format_planning_start(self) -> str:
        """格式化开始规划阶段"""
        self.current_status.phase = ExecutionPhase.PLANNING
        prefix = "\n\n" if self.config.enable_emojis else "\n"
        content = f"{prefix}{self.config.phase_texts.get('planning', '制定计划...')}\n"
        
        response = self._create_base_response(
            delta_content=content,
            metadata={"status_message": "规划中"}
        )
        return self._format_sse_data(response)
    
    def format_plan_generated(self, plan_steps: List[str]) -> str:
        """格式化生成的计划"""
        self.plan_steps = plan_steps
        self.current_status.total_steps = len(plan_steps)
        
        # 创建优雅的计划展示
        emoji_prefix = "✅ " if self.config.enable_emojis else ""
        rocket_emoji = "🚀 " if self.config.enable_emojis else ""
        
        plan_content = f"\n{emoji_prefix}**执行计划已制定：**\n\n"
        for i, step in enumerate(plan_steps, 1):
            plan_content += f"**步骤 {i}：** {step}\n"
        
        plan_content += f"\n{rocket_emoji}开始执行计划（共 {len(plan_steps)} 个步骤）\n\n"
        
        response = self._create_base_response(
            delta_content=plan_content,
            metadata={
                "status_message": "计划已生成",
                "plan_steps": plan_steps
            }
        )
        return self._format_sse_data(response)
    
    def format_step_start(self, step_index: int, task_description: str) -> str:
        """格式化步骤开始"""
        self.current_status.phase = ExecutionPhase.EXECUTING
        self.current_status.step_index = step_index
        self.current_status.current_task = task_description
        self.current_status.progress_percentage = int((step_index / self.current_status.total_steps) * 100)
        
        content = f"---\n\n⚡ **执行步骤 {step_index}/{self.current_status.total_steps}：**{task_description}\n\n"
        
        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"执行步骤 {step_index}",
                "current_task": task_description
            }
        )
        return self._format_sse_data(response)
    
    def format_tool_call_start(self, tool_name: str, tool_description: str = None) -> str:
        """格式化工具调用开始"""
        self.current_status.phase = ExecutionPhase.TOOL_CALLING
        self.current_status.tool_name = tool_name
        
        # 美化工具名称显示
        tool_display_name = self._get_tool_display_name(tool_name)
        desc = f" - {tool_description}" if tool_description else ""
        
        content = f"🔧 正在使用 **{tool_display_name}**{desc}...\n"
        
        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"调用工具：{tool_display_name}",
                "tool_name": tool_name
            }
        )
        return self._format_sse_data(response)
    
    def format_tool_result(self, tool_name: str, result_summary: str) -> str:
        """格式化工具执行结果"""
        tool_display_name = self._get_tool_display_name(tool_name)
        
        content = f"✅ **{tool_display_name}** 执行完成\n"
        
        # 如果结果过长，只显示摘要
        if len(result_summary) > 200:
            content += f"📊 获得结果摘要：{result_summary[:200]}...\n\n"
        else:
            content += f"📊 结果：{result_summary}\n\n"
        
        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"工具执行完成：{tool_display_name}",
                "tool_result_summary": result_summary[:500]
            }
        )
        return self._format_sse_data(response)
    
    def format_step_completed(self, step_index: int, step_result: str) -> str:
        """格式化步骤完成"""
        self.completed_steps.append(self.plan_steps[step_index - 1] if step_index <= len(self.plan_steps) else "未知步骤")
        
        content = f"✅ **步骤 {step_index} 完成**\n\n"
        
        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"步骤 {step_index} 已完成",
                "completed_steps": len(self.completed_steps)
            }
        )
        return self._format_sse_data(response)
    
    def format_replanning(self, reason: str) -> str:
        """格式化重新规划"""
        self.current_status.phase = ExecutionPhase.REPLANNING
        
        content = f"\n🔄 **需要调整计划**\n💡 原因：{reason}\n📋 正在重新制定计划...\n\n"
        
        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": "重新规划中",
                "replan_reason": reason
            }
        )
        return self._format_sse_data(response)
    
    def format_final_answer_start(self) -> str:
        """格式化开始生成最终答案"""
        self.current_status.phase = ExecutionPhase.FINALIZING
        
        content = "\n---\n\n🎯 **正在整理最终答案...**\n\n"
        
        response = self._create_base_response(
            delta_content=content,
            metadata={"status_message": "生成最终答案中"}
        )
        return self._format_sse_data(response)
    
    def format_final_content(self, content: str) -> str:
        """格式化最终内容"""
        response = self._create_base_response(
            delta_content=content,
            metadata={"status_message": "输出最终答案"}
        )
        return self._format_sse_data(response)
    
    def format_completion(self) -> str:
        """格式化完成"""
        self.current_status.phase = ExecutionPhase.COMPLETED
        self.current_status.progress_percentage = 100
        
        emoji_prefix = "✨ " if self.config.enable_emojis else ""
        chart_emoji = "📊 " if self.config.enable_emojis else ""
        clock_emoji = "⏱️ " if self.config.enable_emojis else ""
        
        summary_content = f"\n\n---\n\n{emoji_prefix}**任务完成！**\n"
        summary_content += f"{chart_emoji}总共执行了 {len(self.completed_steps)} 个步骤\n"
        
        if self.config.show_timing:
            execution_time = datetime.now() - self.start_time
            minutes, seconds = divmod(execution_time.total_seconds(), 60)
            time_str = f"{int(minutes)}分{int(seconds)}秒" if minutes > 0 else f"{int(seconds)}秒"
            summary_content += f"{clock_emoji}执行时间：{time_str}\n"
        
        response = self._create_base_response(
            delta_content=summary_content,
            finish_reason="stop",
            metadata={
                "status_message": "任务完成",
                "total_completed_steps": len(self.completed_steps)
            }
        )
        return self._format_sse_data(response)
    
    def _get_tool_display_name(self, tool_name: str) -> str:
        """获取工具的友好显示名称"""
        return self.config.tool_display_names.get(tool_name, tool_name)
