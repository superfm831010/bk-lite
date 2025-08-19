"""
传统 Plan and Execute Agent 响应的优雅格式化器

为非 SSE 接口提供更清晰的结构化输出
"""
from typing import Dict, Any, List
from datetime import datetime

from src.web.entity.agent.plan_and_execute_agent.plan_and_execute_agent_response import PlanAndExecuteAgentResponse


class PlanExecuteResponseFormatter:
    """Plan and Execute Agent 响应格式化器"""
    
    @staticmethod
    def format_response(raw_response: PlanAndExecuteAgentResponse) -> Dict[str, Any]:
        """
        格式化 Plan and Execute Agent 的响应为更优雅的结构
        
        Args:
            raw_response: 原始响应对象
            
        Returns:
            格式化后的响应字典
        """
        try:
            # 提取执行摘要信息
            execution_summary = PlanExecuteResponseFormatter._extract_execution_summary(raw_response)
            
            formatted_response = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "execution_summary": execution_summary,
                "final_answer": raw_response.response or "执行完成",
                "raw_response": raw_response.model_dump() if hasattr(raw_response, 'model_dump') else str(raw_response)
            }
            
            return formatted_response
            
        except Exception as e:
            return {
                "success": False,
                "timestamp": datetime.now().isoformat(),
                "error": f"响应格式化失败: {str(e)}",
                "raw_response": raw_response.model_dump() if hasattr(raw_response, 'model_dump') else str(raw_response)
            }
    
    @staticmethod
    def _extract_execution_summary(response: PlanAndExecuteAgentResponse) -> Dict[str, Any]:
        """提取执行摘要信息"""
        summary = {
            "total_steps": 0,
            "completed_steps": 0,
            "tools_used": [],
            "execution_time": "未知",
            "status": "completed"
        }
        
        try:
            # 尝试从响应中提取相关信息
            response_dict = response.model_dump() if hasattr(response, 'model_dump') else {}
            
            # 提取步骤信息
            if "plan" in response_dict:
                plan = response_dict.get("plan", [])
                summary["total_steps"] = len(plan) if isinstance(plan, list) else 0
            
            if "past_steps" in response_dict:
                past_steps = response_dict.get("past_steps", [])
                summary["completed_steps"] = len(past_steps) if isinstance(past_steps, list) else 0
            
            # 提取使用的工具
            summary["tools_used"] = PlanExecuteResponseFormatter._extract_tools_used(response_dict)
            
        except Exception:
            # 如果提取失败，返回基本摘要
            pass
        
        return summary
    
    @staticmethod
    def _extract_tools_used(response_dict: Dict[str, Any]) -> List[str]:
        """从响应中提取使用的工具列表"""
        tools_used = set()
        
        try:
            # 从消息中提取工具使用信息
            messages = response_dict.get("messages", [])
            for message in messages:
                if isinstance(message, dict):
                    # 检查工具调用
                    if message.get("type") == "tool" or "tool_calls" in message:
                        tool_name = message.get("name") or message.get("tool_name")
                        if tool_name:
                            tools_used.add(tool_name)
            
            # 从过去的步骤中提取工具信息
            past_steps = response_dict.get("past_steps", [])
            for step in past_steps:
                if isinstance(step, (list, tuple)) and len(step) >= 2:
                    step_description = str(step[0])
                    step_result = str(step[1])
                    
                    # 简单的工具检测
                    if "搜索" in step_description or "search" in step_description.lower():
                        tools_used.add("search")
                    if "计算" in step_description or "calculate" in step_description.lower():
                        tools_used.add("calculator")
                    if "网页" in step_description or "web" in step_description.lower():
                        tools_used.add("web_browser")
        
        except Exception:
            pass
        
        return list(tools_used)
