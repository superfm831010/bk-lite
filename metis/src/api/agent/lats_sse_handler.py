"""
LATS Agent SSE 处理器 - 优化版本

提供简洁、高效的 LATS 搜索流式响应处理
重点优化用户体验，减少冗余代码，提高可维护性
防止消息错乱，确保流式输出的顺序性和稳定性
"""
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime

from sanic.log import logger
from src.api.agent.lats_sse_formatter import LatsSSEFormatter


class LatsSSEHandler:
    """LATS SSE 处理器 - 优化版本"""

    def __init__(self, chat_id: str, model: str):
        self.chat_id = chat_id
        self.model = model
        self.formatter = LatsSSEFormatter(chat_id, model)
        self.sent_messages = set()  # 防重复
        self.is_final_answer_started = False
        self._output_lock = asyncio.Lock()  # 添加输出锁，防止并发错乱

    async def send_sse(self, res, message: str) -> None:
        """发送 SSE 消息（线程安全，去重）"""
        if not message:
            return

        async with self._output_lock:  # 确保消息按顺序发送
            if message not in self.sent_messages:
                try:
                    await res.write(message.encode('utf-8'))
                    self.sent_messages.add(message)
                    # 提取消息内容的前50个字符用于日志
                    content_preview = message[:50].replace('\n', ' ').strip()
                    logger.info(f"[LATS SSE] 发送消息: {content_preview}...")
                except Exception as e:
                    logger.error(f"[LATS SSE] 发送消息失败: {e}")
            else:
                logger.debug(f"[LATS SSE] 跳过重复消息: {message[:30]}...")

    async def handle_search_flow(self, res, workflow, body) -> None:
        """处理搜索流程"""
        try:
            logger.info(f"[LATS SSE] 开始处理搜索流程，chat_id: {self.chat_id}")

            # 发送初始化消息
            await self.send_sse(res, self.formatter.format_initialization())
            await self.send_sse(res, self.formatter.format_initial_generation())

            # 处理搜索流
            iteration_count = 0
            async for chunk in await workflow.stream(body):
                await self.process_chunk(res, chunk, iteration_count)

                # 检查是否是新的迭代
                if self._is_new_iteration(chunk):
                    iteration_count += 1

            # 发送完成消息
            await self.send_completion(res)

            logger.info(f"[LATS SSE] 搜索流程处理完成，chat_id: {self.chat_id}")

        except Exception as e:
            logger.error(f"[LATS SSE] 处理出错: {str(e)}", exc_info=True)
            await self.send_sse(res, self.formatter.format_error(str(e)))

    async def process_chunk(self, res, chunk, iteration_count: int) -> None:
        """处理数据块"""
        try:
            logger.debug(f"[LATS SSE] 处理chunk: {type(chunk).__name__}")

            # 处理最终状态
            if self._is_final_state(chunk):
                await self.handle_final_state(res, chunk)
                return

            # 处理评估结果
            if self._is_evaluation_results(chunk):
                await self.handle_evaluation_results(res, chunk['evaluation_results'])
                return

            # 处理节点转换
            if self._is_node_transition(chunk):
                await self.handle_node_transition(res, chunk, iteration_count)
                return

            # 处理消息流
            if self._is_message_stream(chunk):
                await self.handle_message_stream(res, chunk)
                return

            # 处理其他可能的数据类型
            if isinstance(chunk, dict):
                await self.handle_dict_chunk(res, chunk)

        except Exception as e:
            logger.error(f"[LATS SSE] 处理chunk出错: {e}")

    async def handle_dict_chunk(self, res, chunk: dict) -> None:
        """处理字典类型的数据块"""
        # 检查是否包含思考或反思内容
        if 'thought' in chunk or 'thinking' in chunk:
            thought_content = chunk.get('thought') or chunk.get('thinking', '')
            if thought_content:
                await self.send_sse(res, self.formatter.format_thinking_process(str(thought_content)))

        elif 'reflection' in chunk:
            reflection_content = chunk.get('reflection', '')
            score = chunk.get('score')
            if reflection_content:
                await self.send_sse(res, self.formatter.format_reflection(str(reflection_content), score))

    def _is_final_state(self, chunk) -> bool:
        """检查是否为最终状态"""
        return isinstance(chunk, dict) and 'messages' in chunk and 'root' in chunk

    def _is_evaluation_results(self, chunk) -> bool:
        """检查是否为评估结果"""
        return isinstance(chunk, dict) and 'evaluation_results' in chunk

    def _is_node_transition(self, chunk) -> bool:
        """检查是否为节点转换"""
        return isinstance(chunk, dict) and len(chunk) == 1

    def _is_message_stream(self, chunk) -> bool:
        """检查是否为消息流"""
        return isinstance(chunk, (tuple, list)) and len(chunk) > 0

    def _is_new_iteration(self, chunk) -> bool:
        """检查是否为新迭代"""
        return (isinstance(chunk, dict) and 'expand' in chunk) or \
               (self._is_node_transition(chunk) and 'expand' in chunk)

    async def handle_final_state(self, res, chunk) -> None:
        """处理最终状态"""
        root_node = chunk.get('root')
        messages = chunk.get('messages', [])

        if not (root_node and messages):
            return

        # 检查是否找到解决方案
        if hasattr(root_node, 'is_solved') and root_node.is_solved:
            # 获取最佳评分
            best_score = 10  # 默认高分
            if hasattr(root_node, 'reflection') and root_node.reflection:
                best_score = root_node.reflection.score

            await self.send_sse(res, self.formatter.format_solution_found(best_score))

        # 开始最终答案
        if not self.is_final_answer_started:
            await self.send_sse(res, self.formatter.format_final_answer_start())
            self.is_final_answer_started = True

        # 输出最终内容
        if messages:
            final_message = messages[-1]
            if hasattr(final_message, 'content') and final_message.content:
                content = f"\n\n🎯 **LATS 解决方案**\n\n{final_message.content}\n\n"
                await self.send_sse(res, self.formatter.format_content(content))

    async def handle_evaluation_results(self, res, evaluations: List[Dict[str, Any]]) -> None:
        """处理评估结果"""
        if evaluations:
            logger.info(f"[LATS SSE] 展示 {len(evaluations)} 个候选方案评估结果")
            await self.send_sse(res, self.formatter.format_candidates_evaluation(evaluations))

    async def handle_node_transition(self, res, chunk, iteration_count: int) -> None:
        """处理节点转换"""
        node_name = next(iter(chunk.keys()))
        node_data = chunk[node_name]

        if node_name == "generate_initial_response":
            # 输出初始响应生成的思考过程
            await self.send_sse(res, self.formatter.format_content("\n🤔 **分析问题，生成初始回答...**\n\n"))
        elif node_name == "expand":
            await self.send_sse(res, self.formatter.format_search_iteration(iteration_count + 1))
        elif node_name == "tools":
            await self.send_sse(res, self.formatter.format_tool_execution("search_tool"))
        elif node_name == "reflect":
            await self.send_sse(res, self.formatter.format_content("\n🔍 **评估当前解决方案质量...**\n\n"))
        elif node_name == "should_continue":
            await self.send_sse(res, self.formatter.format_content("\n⚖️ **判断是否需要继续搜索...**\n\n"))
        else:
            # 输出其他节点的处理信息
            await self.send_sse(res, self.formatter.format_content(f"\n🔄 **执行 {node_name} 节点...**\n\n"))

    async def handle_message_stream(self, res, chunk) -> None:
        """处理消息流"""
        message = chunk[0] if chunk else None
        if not message:
            return

        message_type = type(message).__name__
        logger.debug(f"[LATS SSE] 处理消息类型: {message_type}")

        # 处理 AI 消息块
        if message_type == "AIMessageChunk" and hasattr(message, 'content') and message.content:
            await self.send_sse(res, self.formatter.format_content(message.content))

        # 处理工具消息 - 展示工具调用的思考过程
        elif "Tool" in message_type and "Message" in message_type:
            if hasattr(message, 'content') and message.content:
                tool_content = message.content
                if tool_content and len(tool_content) > 10:  # 避免输出过短的无意义内容
                    await self.send_sse(res, self.formatter.format_content(f"\n\n🔧 **工具执行结果：**\n\n{tool_content}\n\n"))
            elif hasattr(message, 'name'):
                tool_name = getattr(message, 'name', 'unknown_tool')
                await self.send_sse(res, self.formatter.format_tool_execution(tool_name))

    async def send_completion(self, res) -> None:
        """发送完成消息"""
        try:
            # 发送完成统计
            await self.send_sse(res, self.formatter.format_completion())

            # 发送结束信号
            end_response = {
                "id": self.chat_id,
                "object": "chat.completion.chunk",
                "created": int(datetime.now().timestamp()),
                "model": self.model,
                "choices": [{"delta": {}, "index": 0, "finish_reason": "stop"}]
            }

            json_str = json.dumps(
                end_response, ensure_ascii=False, separators=(',', ':'))

            async with self._output_lock:  # 确保结束信号按顺序发送
                await res.write(f"data: {json_str}\n\n".encode('utf-8'))
                await res.write("data: [DONE]\n\n".encode('utf-8'))

        except Exception as e:
            logger.error(f"[LATS SSE] 发送完成消息失败: {e}")


async def stream_lats_response(workflow, body: Dict[str, Any], chat_id: str, model: str, res) -> None:
    """
    优化的 LATS Agent 流式响应处理函数

    简化逻辑，提升性能，优化用户体验
    防止消息错乱，确保输出顺序
    """
    handler = LatsSSEHandler(chat_id, model)
    await handler.handle_search_flow(res, workflow, body)
