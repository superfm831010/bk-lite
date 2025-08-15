"""
LATS Agent SSE 处理器 - 优化版本

提供简洁、高效的 LATS 搜索流式响应处理，
支持详细的评价表展示和优雅的用户体验
"""
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from sanic.log import logger
from src.api.agent.lats_sse_formatter import LatsSSEFormatter, SearchPhase
from src.api.agent.sse_config import DEFAULT_SSE_CONFIG


class LatsSSEHandler:
    """LATS SSE 处理器，负责管理搜索过程的流式输出"""

    def __init__(self, chat_id: str, model: str):
        self.chat_id = chat_id
        self.model = model
        self.formatter = LatsSSEFormatter(chat_id, model, DEFAULT_SSE_CONFIG)
        self.sent_contents = set()  # 去重
        self.iteration_counter = 0

    async def send_message(self, res, content: str) -> None:
        """发送SSE消息并去重"""
        if content and content not in self.sent_contents:
            await res.write(content.encode('utf-8'))
            self.sent_contents.add(content)
            await asyncio.sleep(0.1)  # 避免消息发送过快

    async def handle_initial_generation(self, res) -> None:
        """处理初始化和初始生成阶段"""
        await self.send_message(res, self.formatter.format_initialization())
        await self.send_message(res, self.formatter.format_initial_generation_start())

    async def handle_evaluation_results(self, res, evaluations: List[Dict[str, Any]]) -> None:
        """处理并展示评价结果表格"""
        if not evaluations:
            return

        logger.info(f"[LATS SSE] 展示{len(evaluations)}个候选方案的评价结果")

        # 显示评价表开始
        await self.send_message(res, self.formatter.format_candidates_evaluation_start(len(evaluations)))

        # 显示详细的评价表格
        detailed_table = self.formatter.format_detailed_evaluation_table(
            evaluations)
        await self.send_message(res, self.formatter.format_final_content(detailed_table))

        # 显示评价结果汇总
        await self.send_message(res, self.formatter.format_candidates_evaluation_results(evaluations))

    async def handle_final_state(self, res, root_node, messages: List) -> None:
        """处理最终状态"""
        if not (root_node and hasattr(root_node, 'is_solved')):
            return

        logger.info(f"[LATS SSE] 搜索完成，找到解决方案: {root_node.is_solved}")

        if messages:
            final_message = messages[-1]
            if hasattr(final_message, 'content') and final_message.content:
                # 根据是否解决问题选择不同的展示方式
                if root_node.is_solved:
                    tree_stats = {
                        'nodes_explored': getattr(root_node, 'height', 0),
                        'tree_height': getattr(root_node, 'height', 0)
                    }

                    # 获取最佳评分
                    best_score = getattr(root_node, 'reflection', None)
                    score = best_score.score if best_score else 10

                    await self.send_message(res,
                                            self.formatter.format_solution_found(score, final_message.content, tree_stats))

                    await self.send_message(res, self.formatter.format_final_answer_start())

                    content = f"\n\n🎯 **LATS 最终解决方案**\n\n{final_message.content}\n\n"
                else:
                    content = f"\n\n💡 **LATS 最佳候选答案**\n\n{final_message.content}\n\n"

                await self.send_message(res, self.formatter.format_final_content(content))

    async def handle_node_transition(self, res, node_name: str) -> None:
        """处理节点流转"""
        if node_name == "generate_initial_response":
            await self.send_message(res, self.formatter.format_initial_generation_start())
        elif node_name == "expand":
            self.iteration_counter += 1
            await self.send_message(res,
                                    self.formatter.format_tree_search_iteration_start(self.iteration_counter, 0, 0))
        elif node_name == "tools":
            await self.send_message(res,
                                    self.formatter.format_tool_call_start("search_tool", "获取相关信息"))

    async def handle_tool_message(self, res, message_type: str) -> None:
        """处理工具消息"""
        if "Tool" in message_type and "Message" in message_type:
            await self.send_message(res,
                                    self.formatter.format_tool_result("search_tool", "工具执行完成，已获取相关信息"))

    async def process_chunk(self, res, chunk) -> None:
        """处理单个数据块"""
        logger.debug(f"[LATS SSE] 处理chunk类型: {type(chunk).__name__}")

        # 处理最终状态
        if isinstance(chunk, dict) and 'messages' in chunk and 'root' in chunk:
            await self.handle_final_state(res, chunk.get('root'), chunk.get('messages', []))
            return

        # 处理评价结果状态
        if isinstance(chunk, dict) and 'evaluation_results' in chunk:
            evaluation_results = chunk.get('evaluation_results', [])
            if evaluation_results:
                await self.handle_evaluation_results(res, evaluation_results)
            return

        # 处理节点流转
        if isinstance(chunk, dict) and len(chunk) == 1:
            node_name = next(iter(chunk.keys()))
            await self.handle_node_transition(res, node_name)
            return

        # 处理消息流
        if isinstance(chunk, (tuple, list)) and len(chunk) > 0:
            message = chunk[0]
            if message is None:
                return

            message_type = type(message).__name__

            # 直接转发 AI 消息块
            if message_type == "AIMessageChunk" and hasattr(message, 'content'):
                content = self.formatter.format_final_content(message.content)
                await self.send_message(res, content)
                logger.debug(
                    f"[LATS SSE] 转发AIMessageChunk: {repr(message.content)}")

            # 处理工具消息
            await self.handle_tool_message(res, message_type)

    async def send_completion_and_end(self, res) -> None:
        """发送完成消息和结束标志"""
        final_stats = {
            'iterations': self.iteration_counter,
            'nodes_explored': self.iteration_counter * 5,  # 估算
            'tree_height': min(self.iteration_counter + 1, 5),
            'best_score': 8.5  # 估算
        }

        await self.send_message(res, self.formatter.format_completion(final_stats))

        # 发送结束标志
        end_response = {
            "id": self.chat_id,
            "object": "chat.completion.chunk",
            "created": int(datetime.now().timestamp()),
            "model": self.model,
            "choices": [{"delta": {}, "index": 0, "finish_reason": "stop"}]
        }

        json_str = json.dumps(
            end_response, ensure_ascii=False, separators=(',', ':'))
        await res.write(f"data: {json_str}\n\n".encode('utf-8'))
        await res.write("data: [DONE]\n\n".encode('utf-8'))

    async def handle_error(self, res, error_msg: str) -> None:
        """处理错误情况"""
        error_content = f"\n\n---\n\n❌ **LATS 搜索遇到问题**\n\n"
        error_content += f"🔧 **错误信息：** {error_msg}\n\n"
        error_content += f"💡 **建议：** 请稍后重试或联系技术支持"

        content = self.formatter.format_final_content(error_content)
        await self.send_message(res, content)


async def stream_lats_response(workflow, body: Dict[str, Any], chat_id: str, model: str, res) -> None:
    """
    简化的 LATS Agent 流式响应处理函数

    Args:
        workflow: LATS 工作流实例
        body: 请求体
        chat_id: 聊天ID
        model: 模型名称
        res: 响应流对象
    """
    handler = LatsSSEHandler(chat_id, model)

    try:
        logger.info(f"[LATS SSE] 开始流式处理，chat_id: {chat_id}")

        # 初始化
        await handler.handle_initial_generation(res)

        # 获取并处理流式迭代器
        stream_iter = await workflow.stream(body)

        async for chunk in stream_iter:
            await handler.process_chunk(res, chunk)

        # 发送完成消息
        await handler.send_completion_and_end(res)

        logger.info(f"[LATS SSE] 流式处理完成，chat_id: {chat_id}")

    except Exception as e:
        logger.error(f"[LATS SSE] 处理过程中出错: {str(e)}", exc_info=True)
        await handler.handle_error(res, str(e))
