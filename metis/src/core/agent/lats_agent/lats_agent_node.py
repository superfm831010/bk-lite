"""
LATS Agent 节点 - 简化优化版本

优化 LATS Agent 核心逻辑，提升代码可读性和性能
减少冗余代码，保持核心功能的完整性
"""
from collections import defaultdict
from typing import List, Tuple

from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.output_parsers import JsonOutputToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from sanic.log import logger

from src.core.agent.lats_agent.lats_agent_state import LatsAgentState, Node, Reflection
from src.core.llm.node.tools_node import ToolsNodes
from src.core.sanic_plus.utils.template_loader import TemplateLoader


class LatsAgentNode(ToolsNodes):
    """LATS Agent 节点处理器 - 优化版本"""

    # 核心配置
    MAX_CANDIDATES = 5
    MAX_TREE_HEIGHT = 5
    EXPLORATION_WEIGHT = 1.0

    def get_reflection_chain(self, state: LatsAgentState, config: RunnableConfig):
        """获取反思评估链"""
        async def reflection_chain_async(inputs):
            llm = self.get_llm_client(
                config["configurable"]["graph_request"], disable_stream=True)

            system_message = TemplateLoader.render_template(
                "prompts/lats_agent/reflection_evaluation")
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_message),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="candidate"),
            ])

            result = await self.call_with_structured_output(
                llm=llm, prompt=prompt, pydantic_model=Reflection, messages=inputs
            )
            return result

        return reflection_chain_async

    def get_expansion_chain(self, state: LatsAgentState, config: RunnableConfig):
        """获取候选生成链"""
        def generate_candidates(messages) -> List[BaseMessage]:
            llm = self.get_llm_client(
                config["configurable"]["graph_request"], disable_stream=True)
            bound_kwargs = llm.bind_tools(tools=self.tools).kwargs

            candidates = []
            logger.debug(f"生成 {self.MAX_CANDIDATES} 个候选解决方案")

            for i in range(self.MAX_CANDIDATES):
                chat_result = llm.generate(
                    [messages.to_messages()],
                    callbacks=[],
                    run_name=f"GenerateCandidate_{i + 1}",
                    **bound_kwargs,
                )
                candidate = chat_result.generations[0][0].message
                candidates.append(candidate)

                # 统计 token 使用
                if hasattr(candidate, 'usage_metadata'):
                    self.tools_prompt_tokens += candidate.usage_metadata.get(
                        'input_tokens', 0)
                    self.tools_completions_tokens += candidate.usage_metadata.get(
                        'output_tokens', 0)

            return candidates

        system_message = TemplateLoader.render_template(
            "prompts/lats_agent/candidate_generation")
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="messages", optional=True),
        ])

        return prompt_template | generate_candidates

    def select(self, root: Node) -> Node:
        """使用 UCB 算法选择最佳节点"""
        if not root.children:
            return root

        node = root
        while node.children:
            max_child = max(
                node.children,
                key=lambda child: child.upper_confidence_bound(
                    self.EXPLORATION_WEIGHT)
            )
            node = max_child

        logger.debug(f"选择深度为 {node.depth} 的节点")
        return node

    async def _process_candidates(
        self,
        candidates: List[BaseMessage],
        state: LatsAgentState,
        config: RunnableConfig
    ) -> Tuple[List[List[BaseMessage]], List[Reflection]]:
        """处理候选方案，执行工具调用和评估"""
        # 解析工具调用
        parser = JsonOutputToolsParser(return_id=True)
        parsed_tool_calls = parser.batch(candidates)

        # 执行工具调用
        tool_node = ToolNode(self.tools, handle_tool_errors=True)
        collected_responses = defaultdict(list)

        for candidate_idx, tool_calls in enumerate(parsed_tool_calls):
            for tool_call in tool_calls:
                try:
                    response = tool_node.invoke({
                        "messages": [AIMessage(
                            content="",
                            tool_calls=[{
                                "name": tool_call["type"],
                                "args": tool_call["args"],
                                "id": tool_call["id"],
                            }]
                        )]
                    })
                    collected_responses[candidate_idx].append(
                        response["messages"][0])
                except Exception as e:
                    logger.warning(f"工具调用失败: {tool_call['type']}, 错误: {e}")
                    collected_responses[candidate_idx].append(
                        AIMessage(content="工具调用失败"))

        # 组合消息
        output_messages = []
        for idx, candidate in enumerate(candidates):
            output_messages.append([candidate] + collected_responses[idx])

        # 反思评估
        user_message = config["configurable"]["graph_request"].user_message
        reflection_func = self.get_reflection_chain(state, config)

        import asyncio
        reflection_inputs = [
            {"input": user_message, "candidate": messages}
            for messages in output_messages
        ]
        reflections = await asyncio.gather(*[
            reflection_func(inputs) for inputs in reflection_inputs
        ])

        # 记录评估结果（简化版）
        self._log_evaluation_summary(reflections)

        # 高分直接标记为解决方案
        for reflection in reflections:
            if reflection.score >= 9:
                reflection.found_solution = True

        return output_messages, reflections

    def _log_evaluation_summary(self, reflections: List[Reflection]) -> None:
        """记录评估摘要"""
        if not reflections:
            return

        max_score = max(r.score for r in reflections)
        solved_count = sum(1 for r in reflections if r.found_solution)
        avg_score = sum(r.score for r in reflections) / len(reflections)

        logger.info(
            f"📊 评估完成 | 候选数: {len(reflections)} | "
            f"最高分: {max_score}/10 | 平均分: {avg_score:.1f}/10 | "
            f"解决方案: {solved_count}个"
        )

    async def expand(self, state: LatsAgentState, config: RunnableConfig) -> LatsAgentState:
        """扩展搜索树"""
        logger.info("🌳 开始扩展搜索树")

        root = state["root"]
        if not root:
            logger.error("搜索树根节点未初始化")
            return state

        # 选择最佳候选节点
        best_candidate = self.select(root)
        messages = best_candidate.get_trajectory()

        # 生成新候选
        user_message = config["configurable"]["graph_request"].user_message
        new_candidates = self.get_expansion_chain(state, config).invoke({
            "input": user_message,
            "messages": messages
        })

        # 处理候选并评估
        output_messages, reflections = await self._process_candidates(
            new_candidates, state, config
        )

        # 添加评估结果到状态
        state['evaluation_results'] = [
            {
                'index': i + 1,
                'score': r.score,
                'found_solution': r.found_solution,
                'reflections': r.reflections,
                'message_content': output_messages[i][-1].content if output_messages[i] else ""
            }
            for i, r in enumerate(reflections)
        ]

        # 扩展搜索树
        child_nodes = [
            Node(cand, parent=best_candidate, reflection=reflection)
            for cand, reflection in zip(output_messages, reflections)
        ]
        best_candidate.children.extend(child_nodes)

        # 检查解决方案
        solution_nodes = [node for node, r in zip(
            child_nodes, reflections) if r.found_solution]
        if solution_nodes:
            best_solution = max(
                solution_nodes, key=lambda node: node.reflection.score)

            logger.info(f"🎉 找到解决方案! 评分: {best_solution.reflection.score}/10")

            # 生成最终答案
            final_answer = await self._generate_final_answer(best_solution, config)
            state["messages"].append(final_answer)
            root._is_solved = True
        else:
            # 添加最佳中间结果
            if child_nodes:
                best_node = max(
                    child_nodes, key=lambda node: node.reflection.score)
                if best_node.reflection.score >= 7:
                    best_message = best_node.get_trajectory(
                        include_reflections=False)[-1]
                    state["messages"].append(best_message)
                    logger.info(
                        f"⭐ 添加高质量中间结果 (评分: {best_node.reflection.score}/10)")

        return state

    async def generate_final_answer(self, state: LatsAgentState, config: RunnableConfig) -> dict:
        """生成最终答案节点"""
        logger.info("📝 生成最终总结答案")

        root = state["root"]

        # 生成最终答案
        final_answer = await self._generate_final_answer(root, config)

        # 将最终答案添加到消息列表
        state["messages"].append(final_answer)

        logger.info("✅ 最终答案生成完成")

        return state

    async def _generate_final_answer(self, solution_node: Node, config: RunnableConfig) -> BaseMessage:
        """生成最终答案"""
        llm = self.get_llm_client(config["configurable"]["graph_request"])

        system_message = TemplateLoader.render_template(
            "prompts/lats_agent/intelligent_assistant")
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="messages", optional=True),
        ])

        final_solution = solution_node.get_trajectory(
            include_reflections=False)[-1]

        # 安全地提取用户核心问题，过滤敏感系统指令
        user_question = config['configurable']['graph_request'].user_message

        question = TemplateLoader.render_template(
            "prompts/lats_agent/final_answer_synthesis",
            {
                "user_question": user_question,
                "solution_content": final_solution.content
            }
        )

        chain = prompt_template | llm
        return chain.invoke({"input": question})

    def should_continue(self, state: LatsAgentState) -> str:
        """决定是否继续搜索"""
        root = state["root"]

        if root.is_solved:
            logger.info("✅ 找到解决方案，生成最终答案")
            return "generate_final_answer"

        if root.height > self.MAX_TREE_HEIGHT:
            logger.info(f"🛑 达到最大搜索深度 ({self.MAX_TREE_HEIGHT})，生成最终答案")
            return "generate_final_answer"

        return "expand"

    async def generate_initial_response(self, state: LatsAgentState, config: RunnableConfig) -> dict:
        """生成初始响应"""
        logger.info("🌱 生成初始响应")

        # 获取初始回答链
        llm = self.get_llm_client(config["configurable"]["graph_request"])
        system_message = TemplateLoader.render_template(
            "prompts/lats_agent/intelligent_assistant")

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="messages", optional=True),
        ])

        user_message = config["configurable"]["graph_request"].user_message
        initial_chain = prompt_template | llm.bind_tools(tools=self.tools)
        res = initial_chain.invoke({"input": user_message})

        # 执行工具调用
        parser = JsonOutputToolsParser(return_id=True)
        parsed = parser.invoke(res)

        tool_node = ToolNode(self.tools)
        tool_responses = [
            tool_node.invoke({
                "messages": [AIMessage(
                    content="",
                    tool_calls=[
                        {"name": r["type"], "args": r["args"], "id": r["id"]}],
                )]
            })
            for r in parsed
        ]

        # 合并消息
        output_messages = [res] + [tr["messages"][0] for tr in tool_responses]

        # 评估初始响应
        reflection_func = self.get_reflection_chain(state, config)
        reflection = await reflection_func({
            "input": user_message,
            "candidate": output_messages
        })

        # 创建根节点
        root = Node(output_messages, reflection=reflection)
        state['root'] = root

        logger.info(f"📊 初始响应评估 | 评分: {reflection.score}/10")

        # 将初始评估结果添加到状态中，用于流式输出
        # 这个数据会作为独立的chunk被流式传输
        state['initial_evaluation'] = {
            'score': reflection.score,
            'reflections': reflection.reflections,
            'found_solution': reflection.found_solution
        }

        # 添加到消息列表
        if output_messages:
            state["messages"].append(output_messages[-1])

        return state
