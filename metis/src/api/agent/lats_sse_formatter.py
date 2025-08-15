"""
LATS Agent SSE 格式化器

负责将 LATS Agent 的搜索过程格式化为优雅的 SSE 输出，
提供类似 Claude 的用户体验，展示树搜索的探索过程
"""
import json
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum

from sanic.log import logger
from src.api.agent.sse_config import SSEDisplayConfig, DEFAULT_SSE_CONFIG


class SearchPhase(Enum):
    """搜索阶段枚举"""
    INITIALIZING = "initializing"              # 初始化
    GENERATING_INITIAL = "generating_initial"  # 生成初始回答
    EVALUATING_INITIAL = "evaluating_initial"  # 评估初始回答
    TREE_SEARCHING = "tree_searching"          # 树搜索中
    GENERATING_CANDIDATES = "generating_candidates"  # 生成候选方案
    TOOL_CALLING = "tool_calling"              # 工具调用
    EVALUATING_CANDIDATES = "evaluating_candidates"  # 评估候选方案
    SOLUTION_FOUND = "solution_found"          # 找到解决方案
    FINALIZING = "finalizing"                  # 最终化
    COMPLETED = "completed"                    # 已完成


@dataclass
class SearchStatus:
    """搜索状态"""
    phase: SearchPhase
    iteration: int = 0          # 当前迭代轮次
    tree_height: int = 0        # 搜索树高度
    nodes_explored: int = 0     # 已探索节点数
    candidates_generated: int = 0  # 已生成候选数
    best_score: float = 0.0     # 当前最佳评分
    solution_found: bool = False  # 是否找到解决方案
    current_task: str = ""      # 当前任务描述
    tool_name: str = ""         # 当前使用工具


class LatsSSEFormatter:
    """LATS Agent SSE 格式化器"""

    def __init__(self, chat_id: str, model: str, config: SSEDisplayConfig = None):
        self.chat_id = chat_id
        self.model = model
        self.config = config or DEFAULT_SSE_CONFIG
        self.created_time = int(datetime.now().timestamp())
        self.current_status = SearchStatus(SearchPhase.INITIALIZING)
        self.start_time = datetime.now()
        self.iteration_count = 0
        self.explored_nodes = 0
        self.solutions_found = []

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
                "search_phase": self.current_status.phase.value,
                "iteration": self.current_status.iteration,
                "tree_height": self.current_status.tree_height,
                "nodes_explored": self.current_status.nodes_explored,
                "best_score": self.current_status.best_score,
                "solution_found": self.current_status.solution_found,
                **(metadata or {})
            }
        }

        if delta_content is not None:
            response["choices"][0]["delta"]["content"] = delta_content

        return response

    def _format_sse_data(self, response: Dict[str, Any]) -> str:
        """格式化 SSE 数据，确保中文字符正确编码"""
        json_str = json.dumps(
            response, ensure_ascii=False, separators=(',', ':'))
        return f"data: {json_str}\n\n"

    def format_initialization(self) -> str:
        """格式化初始化阶段"""
        self.current_status.phase = SearchPhase.INITIALIZING
        content = "🔍 **正在启动 LATS 智能搜索...**\n\n🧠 初始化语言辅助树搜索引擎\n\n💡 准备生成多个候选解决方案"

        response = self._create_base_response(
            delta_content=content,
            metadata={"status_message": "初始化搜索引擎"}
        )
        return self._format_sse_data(response)

    def format_initial_generation_start(self) -> str:
        """格式化开始生成初始回答"""
        self.current_status.phase = SearchPhase.GENERATING_INITIAL
        content = "\n\n---\n\n🌱 **生成初始解决方案...**\n\n🎯 分析问题并构建第一个候选回答"

        response = self._create_base_response(
            delta_content=content,
            metadata={"status_message": "生成初始回答"}
        )
        return self._format_sse_data(response)

    def format_tool_call_start(self, tool_name: str, tool_description: str = None) -> str:
        """格式化工具调用开始"""
        self.current_status.phase = SearchPhase.TOOL_CALLING
        self.current_status.tool_name = tool_name

        # 美化工具名称显示
        tool_display_name = self._get_tool_display_name(tool_name)
        desc = f" - {tool_description}" if tool_description else ""

        content = f"\n🔧 正在调用 **{tool_display_name}**{desc}...\n"

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
            content += f"📊 获得结果摘要：{result_summary[:200]}...\n"
        else:
            content += f"📊 结果：{result_summary}\n"

        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"工具执行完成：{tool_display_name}",
                "tool_result_summary": result_summary[:500]
            }
        )
        return self._format_sse_data(response)

    def format_initial_evaluation(self, score: float, reflection: str, solution_preview: str = None) -> str:
        """格式化初始回答评估"""
        self.current_status.phase = SearchPhase.EVALUATING_INITIAL
        self.current_status.best_score = score

        # 根据评分显示不同的状态指示
        if score >= 9:
            score_emoji = "🌟"
            score_desc = "优秀"
        elif score >= 7:
            score_emoji = "⭐"
            score_desc = "良好"
        elif score >= 5:
            score_emoji = "⚡"
            score_desc = "一般"
        else:
            score_emoji = "🔍"
            score_desc = "需改进"

        content = f"\n📊 **初始方案评估完成**\n\n{score_emoji} 评分：**{score}/10** ({score_desc})\n"

        # 添加评估摘要
        if reflection:
            reflection_summary = reflection[:100] + \
                "..." if len(reflection) > 100 else reflection
            content += f"💭 评估：{reflection_summary}\n"

        # 如果有解决方案预览，显示片段
        if solution_preview:
            preview = solution_preview[:150] + \
                "..." if len(solution_preview) > 150 else solution_preview
            content += f"\n💡 方案预览：{preview}\n"

        content += f"\n🚀 开始树搜索优化..."

        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"初始评估完成 (评分: {score}/10)",
                "initial_score": score
            }
        )
        return self._format_sse_data(response)

    def format_tree_search_iteration_start(self, iteration: int, tree_height: int, nodes_explored: int) -> str:
        """格式化开始新的搜索迭代"""
        self.current_status.phase = SearchPhase.TREE_SEARCHING
        self.current_status.iteration = iteration
        self.current_status.tree_height = tree_height
        self.current_status.nodes_explored = nodes_explored
        self.iteration_count = iteration

        content = f"\n\n---\n\n🌳 **搜索迭代 #{iteration}**\n\n"
        content += f"📏 树高度：{tree_height} | 🔍 已探索：{nodes_explored} 个节点\n"
        content += f"⚡ 选择最佳路径进行扩展..."

        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"搜索迭代 #{iteration}",
                "iteration": iteration,
                "tree_height": tree_height
            }
        )
        return self._format_sse_data(response)

    def format_candidates_generation_start(self, candidate_count: int = 5) -> str:
        """格式化开始生成候选方案"""
        self.current_status.phase = SearchPhase.GENERATING_CANDIDATES

        content = f"\n🧬 **生成 {candidate_count} 个候选解决方案...**\n\n💭 基于当前最佳路径探索新可能性"

        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"生成 {candidate_count} 个候选方案",
                "candidate_count": candidate_count
            }
        )
        return self._format_sse_data(response)

    def format_candidates_evaluation_start(self, candidate_count: int) -> str:
        """格式化开始评估候选方案"""
        self.current_status.phase = SearchPhase.EVALUATING_CANDIDATES

        content = f"\n📊 **评估 {candidate_count} 个候选方案...**\n\n🤔 分析每个方案的质量和可行性"

        response = self._create_base_response(
            delta_content=content,
            metadata={"status_message": f"评估 {candidate_count} 个候选方案"}
        )
        return self._format_sse_data(response)

    def format_candidates_evaluation_results(self, evaluations: List[Dict[str, Any]]) -> str:
        """格式化候选方案评估结果"""
        best_score = max(eval_data["score"]
                         for eval_data in evaluations) if evaluations else 0
        solutions_count = sum(
            1 for eval_data in evaluations if eval_data.get("found_solution", False))

        self.current_status.best_score = max(
            self.current_status.best_score, best_score)

        content = f"\n📈 **评估结果汇总**\n\n"
        content += f"🏆 最高评分：**{best_score}/10**\n"
        content += f"✅ 找到解决方案：**{solutions_count}** 个\n"

        # 显示前3个最好的候选
        sorted_evals = sorted(
            evaluations, key=lambda x: x["score"], reverse=True)[:3]
        content += f"\n🔝 **前3名候选方案：**\n"
        for i, eval_data in enumerate(sorted_evals, 1):
            status_icon = "🎯" if eval_data.get(
                "found_solution", False) else "💡"
            content += f"   {status_icon} **#{i}**: {eval_data['score']}/10\n"

        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"评估完成 (最佳: {best_score}/10)",
                "best_score": best_score,
                "solutions_found": solutions_count
            }
        )
        return self._format_sse_data(response)

    def format_solution_found(self, score: float, solution_preview: str, tree_stats: Dict[str, Any]) -> str:
        """格式化找到解决方案"""
        self.current_status.phase = SearchPhase.SOLUTION_FOUND
        self.current_status.solution_found = True
        self.current_status.best_score = score

        content = f"\n\n🎉 **找到高质量解决方案！**\n\n"
        content += f"🌟 最终评分：**{score}/10**\n"
        content += f"🌳 搜索统计：{tree_stats.get('nodes_explored', 0)} 个节点，{tree_stats.get('tree_height', 0)} 层深度\n"
        content += f"🔄 搜索迭代：{self.iteration_count} 轮\n\n"
        content += f"🎯 **正在生成最终答案...**"

        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"找到解决方案 (评分: {score}/10)",
                "final_score": score,
                "tree_stats": tree_stats
            }
        )
        return self._format_sse_data(response)

    def format_no_solution_continue(self, best_score: float, iteration: int) -> str:
        """格式化未找到解决方案继续搜索"""
        content = f"\n🔄 **搜索迭代 #{iteration} 完成**\n\n"
        content += f"📊 当前最佳评分：**{best_score}/10**\n"
        content += f"🔍 继续探索更优解决方案..."

        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"继续搜索 (当前最佳: {best_score}/10)",
                "current_best": best_score
            }
        )
        return self._format_sse_data(response)

    def format_final_answer_start(self) -> str:
        """格式化开始生成最终答案"""
        self.current_status.phase = SearchPhase.FINALIZING

        content = "\n\n---\n\n✨ **整理最终答案...**\n\n📝 基于搜索结果生成完整回答"

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

    def format_completion(self, final_stats: Dict[str, Any] = None) -> str:
        """格式化完成"""
        self.current_status.phase = SearchPhase.COMPLETED

        emoji_prefix = "🎊 " if self.config.enable_emojis else ""
        chart_emoji = "📊 " if self.config.enable_emojis else ""
        clock_emoji = "⏱️ " if self.config.enable_emojis else ""
        tree_emoji = "🌳 " if self.config.enable_emojis else ""

        summary_content = f"\n\n---\n\n{emoji_prefix}**LATS 搜索完成！**\n"

        if final_stats:
            summary_content += f"{tree_emoji}搜索统计：\n"
            summary_content += f"   • 迭代轮次：{final_stats.get('iterations', self.iteration_count)}\n"
            summary_content += f"   • 探索节点：{final_stats.get('nodes_explored', self.current_status.nodes_explored)}\n"
            summary_content += f"   • 树高度：{final_stats.get('tree_height', self.current_status.tree_height)}\n"
            summary_content += f"   • 最佳评分：{final_stats.get('best_score', self.current_status.best_score)}/10\n"

        if self.config.show_timing:
            execution_time = datetime.now() - self.start_time
            minutes, seconds = divmod(execution_time.total_seconds(), 60)
            time_str = f"{int(minutes)}分{int(seconds)}秒" if minutes > 0 else f"{int(seconds)}秒"
            summary_content += f"{clock_emoji}执行时间：{time_str}\n"

        response = self._create_base_response(
            delta_content=summary_content,
            finish_reason="stop",
            metadata={
                "status_message": "搜索完成",
                "final_stats": final_stats or {}
            }
        )
        return self._format_sse_data(response)

    def format_search_depth_limit(self, max_depth: int) -> str:
        """格式化搜索深度达到限制"""
        content = f"\n\n🛑 **搜索深度达到限制**\n\n"
        content += f"📏 已探索到最大深度：{max_depth} 层\n"
        content += f"💡 返回当前最佳解决方案"

        response = self._create_base_response(
            delta_content=content,
            metadata={
                "status_message": f"达到最大搜索深度 ({max_depth})",
                "max_depth_reached": True
            }
        )
        return self._format_sse_data(response)

    def _get_tool_display_name(self, tool_name: str) -> str:
        """获取工具的友好显示名称"""
        return self.config.tool_display_names.get(tool_name, tool_name)
