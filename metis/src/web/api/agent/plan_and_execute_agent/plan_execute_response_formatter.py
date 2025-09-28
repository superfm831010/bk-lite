"""
传统 Plan and Execute Agent 响应的优雅格式化器

为非 SSE 接口提供更清晰的结构化输出
"""
from typing import Dict, Any

from src.web.entity.agent.plan_and_execute_agent.plan_and_execute_agent_response import PlanAndExecuteAgentResponse


class PlanExecuteResponseFormatter:
    """Plan and Execute Agent 响应格式化器"""

    @staticmethod
    def format_response(raw_response: PlanAndExecuteAgentResponse) -> Dict[str, Any]:
        """
        格式化 Plan and Execute Agent 的响应为简洁的结构

        Args:
            raw_response: 原始响应对象

        Returns:
            格式化后的响应字典
        """
        try:
            # 返回简洁的格式，类似 BasicLLMResponse
            formatted_response = {
                "message": raw_response.message or "执行完成",
                "total_tokens": raw_response.total_tokens,
                "prompt_tokens": raw_response.prompt_tokens,
                "completion_tokens": raw_response.completion_tokens
            }

            return formatted_response

        except Exception as e:
            return {
                "message": f"响应格式化失败: {str(e)}",
                "total_tokens": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0
            }
