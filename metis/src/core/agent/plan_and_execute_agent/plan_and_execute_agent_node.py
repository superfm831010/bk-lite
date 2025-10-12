from typing import List, Union, Dict, Any, Literal

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langgraph.constants import END
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

from src.core.agent.plan_and_execute_agent.plan_and_execute_agent_state import PlanAndExecuteAgentState
from src.core.llm.node.tools_node import ToolsNodes
from neco.core.utils.template_loader import TemplateLoader


class Plan(BaseModel):
    """代表计划的模型，包含一系列有序步骤"""
    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )


class Response(BaseModel):
    """代表最终用户响应的模型"""
    response: str


class Act(BaseModel):
    """代表AI可能的动作：生成计划或提供最终响应"""
    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
                    "If you need to further use tools to get the answer, use Plan."
    )


class PlanAndExecuteAgentNode(ToolsNodes):
    """Plan and Execute Agent节点实现 - 简化版本

    使用抽象的组合节点大幅简化实现，只保留核心逻辑
    """

    async def planner_node(self, state: PlanAndExecuteAgentState, config: RunnableConfig):
        """生成初始计划步骤 - 使用 chat_node + 结构化输出"""

        # 获取用户消息
        user_message = config["configurable"]["graph_request"].user_message

        # 创建规划提示
        base_instructions = TemplateLoader.render_template(
            "prompts/plan_and_execute_agent/base_planning_instruction",
            {"tools": self.tools}
        )

        # 使用模板系统创建提示
        planner_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=base_instructions),
            MessagesPlaceholder(variable_name="messages"),
        ])

        # 创建人类消息
        human_message = HumanMessage(content=user_message)

        # 获取LLM客户端
        llm = self.get_llm_client(
            config["configurable"]["graph_request"], disable_stream=True)

        # 使用结构化输出生成计划
        self.log(config, f"为任务生成初始计划: {user_message}")
        plan = await self.call_with_structured_output(
            llm=llm,
            prompt=planner_prompt,
            pydantic_model=Plan,
            messages=[human_message],
        )

        # 格式化计划并记录日志
        plan_str = "\n".join([f"- {step}" for step in plan.steps])
        self.log(config, f"生成的初始计划包含 {len(plan.steps)} 个步骤:\n{plan_str}")

        # 创建AI消息并更新状态
        ai_message = AIMessage(
            content=f"已为任务生成计划，包含 {len(plan.steps)} 个步骤:\n{plan_str}")

        return {
            "messages": [ai_message],
            "plan": plan.steps,
            "current_step_index": 0,
            "past_steps": []
        }

    def build_plan_execute_react_nodes(self,
                                       graph_builder: StateGraph,
                                       composite_node_name: str = "plan_execute_agent",
                                       end_node: str = END) -> str:
        """构建计划执行的 ReAct 组合节点

        这个组合节点负责：
        1. 执行当前计划步骤
        2. 根据执行结果决定是否重新规划
        3. 生成最终响应
        """

        # 内部节点名称
        llm_node_name = f"{composite_node_name}_llm"
        tool_node_name = f"{composite_node_name}_tools"

        # 添加 LLM 节点 - 处理步骤执行和重新规划
        async def llm_node(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
            try:
                messages = state["messages"]
                plan = state.get("plan", [])
                past_steps = state.get("past_steps", [])
                current_step_index = state.get("current_step_index", 0)

                self.log(
                    config, f"LLM节点状态 - 计划步骤: {len(plan)}, 已完成步骤: {len(past_steps)}, 当前索引: {current_step_index}")

                # 如果计划已经完成，生成最终响应
                if not plan and past_steps:
                    self.log(config, f"所有计划步骤已完成，开始生成最终响应")
                    return await self._generate_final_response(state, config)

                # 如果没有计划也没有历史，表示需要重新规划
                if not plan and not past_steps:
                    self.log(config, f"没有可执行的计划，开始重新规划")
                    return await self._handle_replan(state, config)

                # 执行当前步骤
                if plan:
                    task = plan[0]
                    self.log(
                        config, f"执行步骤{current_step_index + 1}/{len(past_steps) + len(plan)}: {task}")

                    # 准备任务执行的消息
                    task_message = self._prepare_task_message(
                        state, task, config)

                    # 获取 LLM 并绑定工具
                    graph_request = config["configurable"]["graph_request"]
                    llm = self.get_llm_client(
                        graph_request).bind_tools(self.tools)

                    # 创建执行提示
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", self._get_execution_system_prompt()),
                        MessagesPlaceholder(variable_name="messages"),
                    ])

                    # 调用 LLM 执行任务
                    response = await (prompt | llm).ainvoke({"messages": messages + [task_message]})

                    # 记录执行结果
                    step_result = response.content if response.content else "执行完成"
                    new_past_steps = past_steps + [(task, step_result)]

                    self.log(
                        config, f"步骤 {current_step_index + 1} 执行完成，结果: {step_result[:100]}...")

                    return {
                        "messages": [response],
                        "past_steps": new_past_steps,
                        "current_step_index": current_step_index + 1,
                        "plan": plan[1:],  # 移除已执行的步骤
                    }
                else:
                    # 这种情况理论上不应该发生，但为了安全起见
                    self.log(config, f"意外状态：没有计划步骤可执行")
                    return {"messages": [AIMessage(content="没有更多步骤需要执行")]}

            except Exception as e:
                self.log(config, f"步骤执行失败: {e}")
                return {"messages": [AIMessage(content=f"执行失败: {str(e)}")]}

        graph_builder.add_node(llm_node_name, llm_node)

        # 添加工具节点
        async def tool_node(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
            try:
                tools_node = await self.build_tools_node()
                return await tools_node.ainvoke(state)
            except Exception as e:
                self.log(config, f"工具执行失败: {e}")
                from langchain_core.messages import ToolMessage
                return {"messages": [ToolMessage(content=f"工具执行失败: {str(e)}", tool_call_id="error")]}

        graph_builder.add_node(tool_node_name, tool_node)

        # 条件判断函数
        def should_continue(state: Dict[str, Any]) -> Literal["tools", "continue", "end"]:
            messages = state.get("messages", [])
            plan = state.get("plan", [])
            past_steps = state.get("past_steps", [])

            # 检查是否有最终响应（计划已完成）
            if state.get("response"):
                return "end"  # 结束执行

            # 检查最后一条消息是否有工具调用
            if messages and hasattr(messages[-1], 'tool_calls') and messages[-1].tool_calls:
                return "tools"

            # 检查是否还有未执行的计划步骤
            if plan:
                # 还有步骤需要执行，继续回到LLM节点
                return "continue"

            # 检查是否没有更多计划且有执行历史（应该生成最终响应）
            if not plan and past_steps:
                return "continue"  # 回到LLM生成最终响应

            # 其他情况结束
            return "end"

        # 添加条件边
        graph_builder.add_conditional_edges(
            llm_node_name,
            should_continue,
            {"tools": tool_node_name, "continue": llm_node_name, "end": end_node}
        )

        # 工具执行后回到 LLM
        graph_builder.add_edge(tool_node_name, llm_node_name)

        return llm_node_name  # 返回入口节点

    async def _generate_final_response(self, state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        """生成最终响应"""
        user_message = config["configurable"]["graph_request"].user_message
        past_steps = state.get("past_steps", [])

        # 格式化执行历史
        past_steps_formatted = "\n".join([
            f"步骤 {i + 1}: {step[0]}\n执行结果: {step[1]}\n"
            for i, step in enumerate(past_steps)
        ])

        # 创建最终响应生成的提示
        message_content = TemplateLoader.render_template(
            "prompts/plan_and_execute_agent/final_answer_generation",
            {
                "user_message": user_message,
                "past_steps_formatted": past_steps_formatted
            }
        )

        # 创建系统提示
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个智能助手，需要根据执行结果生成最终答案。请仔细分析所有步骤的执行结果，提取关键信息，给出准确的最终答案。"),
            MessagesPlaceholder(variable_name="messages"),
        ])

        # 获取LLM客户端
        graph_request = config["configurable"]["graph_request"]
        llm = self.get_llm_client(graph_request, disable_stream=True)

        # 生成最终响应
        self.log(config, f"开始生成最终响应，基于 {len(past_steps)} 个已执行步骤")
        response = await (system_prompt | llm).ainvoke({
            "messages": [HumanMessage(content=message_content)]
        })

        final_response = response.content
        self.log(config, f"生成最终响应: {final_response}")

        return {
            "messages": [AIMessage(content=final_response)],
            "response": final_response
        }

    async def _handle_replan(self, state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        """处理重新规划"""
        user_message = config["configurable"]["graph_request"].user_message

        # 创建重新规划的提示
        base_instructions = TemplateLoader.render_template(
            "prompts/plan_and_execute_agent/base_planning_instruction",
            {"tools": self.tools}
        )

        replanning_content = TemplateLoader.render_template(
            "prompts/plan_and_execute_agent/replanning_instruction",
            {"base_instructions": base_instructions}
        )

        # 创建重新规划消息
        message_content = TemplateLoader.render_template(
            "prompts/plan_and_execute_agent/replan_evaluation",
            {"user_message": user_message}
        )

        # 构建提示
        replan_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=replanning_content),
            MessagesPlaceholder(variable_name="messages"),
        ])

        # 获取LLM客户端
        llm = self.get_llm_client(
            config["configurable"]["graph_request"], disable_stream=True)

        # 使用结构化输出
        self.log(config, "开始重新规划")
        output = await self.call_with_structured_output(
            llm=llm,
            prompt=replan_prompt,
            pydantic_model=Act,
            messages=[HumanMessage(content=message_content)],
        )

        if isinstance(output.action, Response):
            # 生成最终响应
            final_response = output.action.response
            self.log(config, f"重新规划后生成最终响应: {final_response}")
            return {
                "messages": [AIMessage(content=final_response)],
                "response": final_response
            }
        else:
            # 生成新计划
            new_plan = output.action.steps
            plan_str = "\n".join([f"- {step}" for step in new_plan])
            self.log(config, f"重新规划结果: 新计划包含 {len(new_plan)} 个步骤")

            return {
                "messages": [AIMessage(content=f"已重新规划任务，新计划：\n{plan_str}")],
                "plan": new_plan,
                "current_step_index": 0
            }

    def _prepare_task_message(self, state: Dict[str, Any], task: str, config: RunnableConfig) -> HumanMessage:
        """准备任务执行消息"""
        plan = state.get("plan", [])
        past_steps = state.get("past_steps", [])
        current_step_index = state.get("current_step_index", 0)

        # 创建完整计划字符串
        full_plan = past_steps + [(f"步骤 {len(past_steps) + 1}", task)] + [(
            f"步骤 {len(past_steps) + i + 2}", step) for i, step in enumerate(plan[1:])]
        plan_str = "\n".join(
            f"{i + 1}. {step[1] if isinstance(step, tuple) else step}" for i, step in enumerate(full_plan))

        # 格式化已完成步骤信息
        past_steps_info = ""
        if past_steps:
            past_steps_info = "\n\n已完成的步骤:\n" + "\n".join([
                f"步骤 {i + 1}: {step[0]}\n结果: {step[1][:200]}..." if len(
                    step[1]) > 200 else f"步骤 {i + 1}: {step[0]}\n结果: {step[1]}"
                for i, step in enumerate(past_steps)
            ])

        # 使用模板生成任务消息
        task_formatted = TemplateLoader.render_template(
            "prompts/plan_and_execute_agent/execute_step_task",
            {
                "plan_str": plan_str,
                "past_steps_info": past_steps_info,
                "current_step_index": current_step_index + 1,
                "total_steps": len(past_steps) + len(plan),
                "task": task
            }
        )

        return HumanMessage(content=task_formatted)

    def _get_execution_system_prompt(self) -> str:
        """获取执行系统提示"""
        return TemplateLoader.render_template(
            'prompts/graph/base_node_system_message', {
                "user_system_message": "你是一个智能助手，负责执行计划中的具体步骤。请仔细分析当前任务，使用合适的工具获取信息，并提供详细的执行结果。"
            }
        )
