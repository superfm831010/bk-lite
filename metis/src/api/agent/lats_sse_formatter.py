
"""
LATS Agent SSE 格式化器 - 简化优化版本

提供简洁、优雅的 LATS 搜索流式响应格式化
重点关注用户体验，减少冗余信息，突出关键内容
"""
import json
from datetime import datetime
from typing import Dict, Any, List
from enum import Enum
from dataclasses import dataclass

from sanic.log import logger


class SearchPhase(Enum):
    """搜索阶段枚举"""
    INITIALIZING = "initializing"
    GENERATING = "generating"
    EVALUATING = "evaluating"
    SEARCHING = "searching"
    TOOL_CALLING = "tool_calling"
    SOLUTION_FOUND = "solution_found"
    COMPLETED = "completed"


@dataclass
class SearchStats:
    """搜索统计信息"""
    iteration: int = 0
    nodes_explored: int = 0
    best_score: float = 0.0
    solutions_found: int = 0


class LatsSSEFormatter:
    """LATS Agent SSE 格式化器 - 优化版本"""

    def __init__(self, chat_id: str, model: str):
        self.chat_id = chat_id
        self.model = model
        self.created_time = int(datetime.now().timestamp())
        self.start_time = datetime.now()
        self.stats = SearchStats()
        self._message_sequence = 0  # 添加消息序列号，确保顺序

    def _create_sse_response(self, content: str = None, finish_reason: str = None,
                             metadata: Dict[str, Any] = None) -> str:
        """创建 SSE 响应数据"""
        self._message_sequence += 1

        response = {
            "id": self.chat_id,
            "object": "chat.completion.chunk",
            "created": self.created_time,
            "model": self.model,
            "choices": [{
                "delta": {"role": "assistant"},
                "index": 0,
                "finish_reason": finish_reason
            }]
        }

        if content:
            response["choices"][0]["delta"]["content"] = content

        if metadata:
            response["metis_metadata"] = {
                **metadata,
                "sequence": self._message_sequence  # 添加序列号
            }

        json_str = json.dumps(
            response, ensure_ascii=False, separators=(',', ':'))
        return f"data: {json_str}\n\n"

    def format_initialization(self) -> str:
        """格式化初始化"""
        content = "🔍 **启动 LATS 智能搜索**\n\n💡 分析问题并生成多个候选解决方案"
        return self._create_sse_response(content, metadata={"phase": "initializing"})

    def format_initial_generation(self) -> str:
        """格式化初始生成"""
        content = "\n\n---\n\n🌱 **生成初始解决方案**\n\n🎯 构建第一个候选回答\n\n"
        return self._create_sse_response(content, metadata={"phase": "generating"})

    def format_tool_execution(self, tool_name: str) -> str:
        """格式化工具执行"""
        tool_display = self._get_tool_display_name(tool_name)
        content = f"\n🔧 **调用 {tool_display}**\n\n💡 正在搜索相关信息..."
        return self._create_sse_response(content, metadata={"phase": "tool_calling", "tool": tool_name})

    def format_thinking_process(self, thought: str) -> str:
        """格式化思考过程"""
        # 清理思考内容，避免过长
        cleaned_thought = thought.strip()
        if len(cleaned_thought) > 800:
            cleaned_thought = cleaned_thought[:800] + "..."

        content = f"\n� **{cleaned_thought}**\n"
        return self._create_sse_response(content, metadata={"phase": "thinking"})

    def format_reflection(self, reflection: str, score: float = None) -> str:
        """格式化反思过程"""
        # 清理反思内容
        cleaned_reflection = reflection.strip()
        if len(cleaned_reflection) > 600:
            cleaned_reflection = cleaned_reflection[:600] + "..."

        content = f"\n📝 **质量评估**\n\n{cleaned_reflection}\n"
        if score is not None:
            emoji = "🌟" if score >= 9 else "⭐" if score >= 8 else "✨" if score >= 6 else "💡"
            status_emoji = "🎯" if score >= 9 else "👍" if score >= 7 else "📈"
            content += f"\n{status_emoji} **评分：{score}/10** {emoji}\n"
        return self._create_sse_response(content, metadata={"phase": "reflecting", "score": score})

    def format_initial_evaluation(self, score: float) -> str:
        """格式化初始评估"""
        self.stats.best_score = score
        emoji = "🌟" if score >= 8 else "⭐" if score >= 6 else "💡"

        content = f"\n📊 **初始评估完成** {emoji}\n\n"
        content += f"📈 评分：**{score}/10**\n"

        # 根据评分决定下一步行动
        if score >= 9:
            content += f"🎉 **高质量方案！无需进一步搜索**"
        elif score >= 7:
            content += f"✨ **良好方案，考虑优化空间**"
        else:
            content += f"🚀 **开始树搜索优化...**"

        return self._create_sse_response(content, metadata={"phase": "evaluating", "score": score})

    def format_search_iteration(self, iteration: int) -> str:
        """格式化搜索迭代"""
        self.stats.iteration = iteration

        content = f"\n\n---\n\n🌳 **搜索迭代 #{iteration}**\n\n"
        content += f"🔍 探索新的解决方案路径..."

        return self._create_sse_response(content, metadata={
            "phase": "searching",
            "iteration": iteration
        })

    def format_candidates_evaluation(self, evaluations: List[Dict[str, Any]]) -> str:
        """格式化候选方案评估（简化版）"""
        if not evaluations:
            return ""

        best_score = max(e.get("score", 0) for e in evaluations)
        solutions_count = sum(
            1 for e in evaluations if e.get("found_solution", False))

        self.stats.best_score = max(self.stats.best_score, best_score)
        self.stats.solutions_found = solutions_count

        content = f"\n📊 **评估 {len(evaluations)} 个候选方案**\n\n"
        content += f"🏆 最高评分：**{best_score}/10**\n"

        if solutions_count > 0:
            content += f"✅ 找到 **{solutions_count}** 个解决方案\n"

        # 只显示前3个最佳候选
        top_candidates = sorted(
            evaluations, key=lambda x: x.get("score", 0), reverse=True)[:3]
        content += f"\n🔝 **优秀候选：**\n"
        for i, candidate in enumerate(top_candidates, 1):
            score = candidate.get("score", 0)
            status = "🎯" if candidate.get("found_solution", False) else "💡"
            content += f"   {status} #{i}: {score}/10\n"

        return self._create_sse_response(content, metadata={
            "phase": "evaluating",
            "best_score": best_score,
            "solutions_found": solutions_count
        })

    def format_solution_found(self, score: float) -> str:
        """格式化找到解决方案"""
        content = f"\n🎉 **找到高质量解决方案！**\n\n"
        content += f"🌟 最终评分：**{score}/10**\n"
        content += f"🔄 搜索迭代：{self.stats.iteration} 轮\n\n"
        content += f"🎯 **生成最终答案...**"

        return self._create_sse_response(content, metadata={
            "phase": "solution_found",
            "final_score": score
        })

    def format_final_answer_start(self) -> str:
        """格式化开始生成最终答案"""
        content = "\n\n---\n\n✨ **整理最终答案**\n\n📝 基于搜索结果生成完整回答"
        return self._create_sse_response(content, metadata={"phase": "finalizing"})

    def format_content(self, content: str) -> str:
        """格式化内容输出"""
        # 保护原始内容，只做基本清理
        if not content:
            return ""

        # 移除可能的控制字符，但保持内容完整
        cleaned_content = content.replace('\x00', '').strip()

        # 不截断内容，保持完整性
        return self._create_sse_response(cleaned_content)

    def format_completion(self) -> str:
        """格式化完成"""
        execution_time = datetime.now() - self.start_time
        time_str = f"{int(execution_time.total_seconds())}秒"

        content = f"\n\n---\n\n🎊 **LATS 搜索完成！**\n\n"
        content += f"📊 **搜索统计：**\n"
        content += f"   • 迭代轮次：{self.stats.iteration}\n"
        content += f"   • 最佳评分：{self.stats.best_score}/10\n"
        content += f"   • 执行时间：{time_str}\n"

        return self._create_sse_response(content, finish_reason="stop", metadata={
            "phase": "completed",
            "stats": {
                "iterations": self.stats.iteration,
                "best_score": self.stats.best_score,
                "execution_time": time_str
            }
        })

    def format_error(self, error_msg: str) -> str:
        """格式化错误"""
        content = f"\n❌ **搜索遇到问题**\n\n🔧 {error_msg}\n\n💡 请稍后重试"
        return self._create_sse_response(content, finish_reason="error")

    def _get_tool_display_name(self, tool_name: str) -> str:
        """获取工具友好显示名称"""
        tool_names = {
            "naive_rag_search": "知识库搜索",
            "web_search": "网络搜索",
            "search_tool": "搜索工具",
            "analysis_tool": "分析工具"
        }
        return tool_names.get(tool_name, tool_name)

    # 保持向后兼容的方法
    def format_initial_generation_start(self) -> str:
        return self.format_initial_generation()

    def format_final_content(self, content: str) -> str:
        return self.format_content(content)

    def format_tool_call_start(self, tool_name: str, description: str = None) -> str:
        return self.format_tool_execution(tool_name)

    def format_candidates_evaluation_results(self, evaluations: List[Dict[str, Any]]) -> str:
        return self.format_candidates_evaluation(evaluations)

    def format_search_iteration(self, iteration: int) -> str:
        """格式化搜索迭代"""
        self.stats.iteration = iteration

        content = f"\n\n---\n\n🌳 **搜索迭代 #{iteration}**\n\n"
        content += f"🔍 探索新的解决方案路径..."

        return self._create_sse_response(content, metadata={
            "phase": "searching",
            "iteration": iteration
        })

    def format_candidates_evaluation(self, evaluations: List[Dict[str, Any]]) -> str:
        """格式化候选方案评估（简化版）"""
        if not evaluations:
            return ""

        best_score = max(e.get("score", 0) for e in evaluations)
        solutions_count = sum(
            1 for e in evaluations if e.get("found_solution", False))

        self.stats.best_score = max(self.stats.best_score, best_score)
        self.stats.solutions_found = solutions_count

        content = f"\n📊 **评估 {len(evaluations)} 个候选方案**\n\n"
        content += f"🏆 最高评分：**{best_score}/10**\n"

        if solutions_count > 0:
            content += f"✅ 找到 **{solutions_count}** 个解决方案\n"

        # 只显示前3个最佳候选
        top_candidates = sorted(
            evaluations, key=lambda x: x.get("score", 0), reverse=True)[:3]
        content += f"\n🔝 **优秀候选：**\n"
        for i, candidate in enumerate(top_candidates, 1):
            score = candidate.get("score", 0)
            status = "🎯" if candidate.get("found_solution", False) else "💡"
            content += f"   {status} #{i}: {score}/10\n"

        return self._create_sse_response(content, metadata={
            "phase": "evaluating",
            "best_score": best_score,
            "solutions_found": solutions_count
        })

    def format_solution_found(self, score: float) -> str:
        """格式化找到解决方案"""
        content = f"\n\n🎉 **找到高质量解决方案！**\n\n"
        content += f"🌟 最终评分：**{score}/10**\n"
        content += f"🔄 搜索迭代：{self.stats.iteration} 轮\n\n"
        content += f"🎯 **生成最终答案...**"

        return self._create_sse_response(content, metadata={
            "phase": "solution_found",
            "final_score": score
        })

    def format_final_answer_start(self) -> str:
        """格式化开始生成最终答案"""
        content = "\n\n---\n\n✨ **整理最终答案**\n\n📝 基于搜索结果生成完整回答"
        return self._create_sse_response(content, metadata={"phase": "finalizing"})

    def format_content(self, content: str) -> str:
        """格式化内容输出"""
        return self._create_sse_response(content)

    def format_completion(self) -> str:
        """格式化完成"""
        execution_time = datetime.now() - self.start_time
        time_str = f"{int(execution_time.total_seconds())}秒"

        content = f"\n\n---\n\n🎊 **LATS 搜索完成！**\n\n"
        content += f"📊 **搜索统计：**\n"
        content += f"   • 迭代轮次：{self.stats.iteration}\n"
        content += f"   • 最佳评分：{self.stats.best_score}/10\n"
        content += f"   • 执行时间：{time_str}\n"

        return self._create_sse_response(content, finish_reason="stop", metadata={
            "phase": "completed",
            "stats": {
                "iterations": self.stats.iteration,
                "best_score": self.stats.best_score,
                "execution_time": time_str
            }
        })

    def format_error(self, error_msg: str) -> str:
        """格式化错误"""
        content = f"\n\n❌ **搜索遇到问题**\n\n🔧 {error_msg}\n\n💡 请稍后重试"
        return self._create_sse_response(content, finish_reason="error")

    def _get_tool_display_name(self, tool_name: str) -> str:
        """获取工具友好显示名称"""
        tool_names = {
            "naive_rag_search": "知识库搜索",
            "web_search": "网络搜索",
            "search_tool": "搜索工具",
            "analysis_tool": "分析工具"
        }
        return tool_names.get(tool_name, tool_name)

    # 保持向后兼容的方法
    def format_initial_generation_start(self) -> str:
        return self.format_initial_generation()

    def format_final_content(self, content: str) -> str:
        return self.format_content(content)

    def format_tool_call_start(self, tool_name: str, description: str = None) -> str:
        return self.format_tool_execution(tool_name)

    def format_candidates_evaluation_results(self, evaluations: List[Dict[str, Any]]) -> str:
        return self.format_candidates_evaluation(evaluations)
