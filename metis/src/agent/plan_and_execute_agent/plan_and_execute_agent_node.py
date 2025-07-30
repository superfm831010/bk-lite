from email import message
from pyexpat.errors import messages
from typing import List, Union, Dict, Any, Optional, Tuple

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langgraph.constants import END
from langgraph.prebuilt import create_react_agent
from sanic.log import logger
from pydantic import BaseModel, Field

from src import summarize
from src.agent.plan_and_execute_agent.plan_and_execute_agent_state import PlanAndExecuteAgentState
from src.core.node.tools_node import ToolsNodes


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
    """Plan and Execute Agent节点实现

    负责管理计划生成、步骤执行和重新规划的逻辑
    """

    async def execute_step(self, state: PlanAndExecuteAgentState, config: RunnableConfig):
        """执行当前计划中的第一个步骤

        Args:
            state: 当前状态
            config: 可运行配置

        Returns:
            包含执行结果的新状态
        """
        messages = state['messages']

        # 检查计划是否为空
        if not state.get("plan"):
            self.log(config, "没有可执行的计划步骤，需要重新规划")
            return {
                "current_step_index": state.get("current_step_index", 0) + 1,
                "replan_needed": True
            }

        plan = state["plan"]
        plan_str = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(plan))

        task = plan[0]
        current_step_index = state.get("current_step_index", 0)
        total_steps = len(plan) + len(state.get("past_steps", []))

        # 获取LLM客户端
        llm = self.get_llm_client(config["configurable"]["graph_request"])

        # 创建ReAct代理
        agent_executor = create_react_agent(llm, self.tools,
                                            prompt=config["configurable"]["graph_request"].system_message_prompt)

        # 格式化任务信息，包含已完成的步骤信息以提供更多上下文
        past_steps_info = ""
        if state.get("past_steps"):
            past_steps_info = "\n\n已完成的步骤:\n" + "\n".join([
                f"步骤 {i + 1}: {step[0]}\n结果: {step[1][:200]}..." if len(
                    step[1]) > 200 else f"步骤 {i + 1}: {step[0]}\n结果: {step[1]}"
                for i, step in enumerate(state["past_steps"])
            ])

        task_formatted = f"""For the following plan:
    {plan_str}\n\n{past_steps_info}\n\nYou are tasked with executing step {current_step_index + 1}/{total_steps}, {task}.
    
如果这是最后一个步骤，请确保提供完整的最终答案。"""

        self.log(
            config, f"执行计划步骤 {current_step_index + 1}/{total_steps}: {task}")

        # 创建人类消息
        human_message = HumanMessage(content=task_formatted)
        messages.append(human_message)

        # 执行代理
        try:
            agent_response = await agent_executor.ainvoke(
                {"messages": messages}
            )
            ai_response = agent_response["messages"][-1]
            step_result = ai_response.content
        except Exception as e:
            step_result = f"执行步骤时发生异常: {e}"
            self.log(config, f"{step_result}, 触发replan")
            ai_response = None

        is_last_step = len(plan) == 1
        response = None

        # 判断是否获得最终答案（只在最后一步）
        if is_last_step and ai_response and ("结果" in ai_response.content or "答案" in ai_response.content):
            response = ai_response.content
            self.log(config, f"检测到最终答案，任务完成")

        # 始终追加 past_steps，异常也记录
        new_past_steps = state.get("past_steps", []) + [(task, step_result)]

        # 如果最后一步且未获得最终答案，或中间步骤异常，需 replan
        replan_needed = False
        if is_last_step and not response:
            replan_needed = True
        if ai_response is None:
            replan_needed = True

        messages.append(ai_response)
        result = {
            "messages": messages,
            "past_steps": new_past_steps,
            "current_step_index": current_step_index + 1,
            "plan": plan[1:],
        }
        if response:
            result["response"] = response
        if replan_needed:
            result["replan_needed"] = True
        return result

    def should_end(self, state: PlanAndExecuteAgentState, config: RunnableConfig):
        """决定是否应该结束图执行

        Args:
            state: 当前状态

        Returns:
            如果有最终响应则结束，否则继续执行
        """
        # 如果有响应，则结束执行
        if state.get("response"):
            self.log(config, f"执行完成，返回最终响应")
            return END

        # 如果计划列表为空且已经执行了一些步骤，需要检查最后一步的执行结果
        if not state.get("plan") and state.get("past_steps"):
            # 检查最后一个执行结果是否包含可能的最终答案
            last_step_result = state["past_steps"][-1][1]

            # 如果最后一步的结果看起来像是最终答案，就直接使用它作为响应
            if "最终结果" in last_step_result or "最终答案" in last_step_result or "任务完成" in last_step_result:
                self.log(config, f"检测到最后一步似乎已完成任务，提取结果作为最终响应")
                return {
                    "response": last_step_result,
                    "messages": [
                        AIMessage(content=f"任务已完成，最终结果：{last_step_result}")
                    ]
                }

            self.log(config, f"计划执行完毕，进行最终结果整理")
            return "replan"

        # 否则继续执行下一步
        self.log(config, f"继续执行下一个计划步骤，剩余步骤数: {len(state.get('plan', []))}")
        return "agent"

    def _create_planning_prompt(self, for_replanning: bool = False) -> ChatPromptTemplate:
        """创建规划提示模板

        Args:
            for_replanning: 是否用于重新规划

        Returns:
            聊天提示模板
        """
        base_instructions = f"""
        为了实现以下目标，制定一个简单的分步计划。以下是你可以使用的工具：{self.tools}
        
        此计划应涉及单独的任务，如果正确执行将产生正确的答案。不要添加任何多余的步骤。
        最后一步的结果应该是最终答案。确保每一步都有所有需要的信息 - 不要跳过步骤。
        """

        if for_replanning:
            template = [
                SystemMessage(content=base_instructions + """
                你的原始计划是：
                {original_plan}
                
                你已经完成了以下步骤：
                {completed_steps}
                
                请相应地更新你的计划。如果不需要更多步骤，你可以直接向用户返回最终结果。
                否则，填写计划。只添加仍然需要完成的步骤。
                不要在计划中包含已完成的步骤。
                
                重要提醒：在提供最终响应时，请确保从执行结果中提取实际的数值或内容，而不是变量名。
                """),
                MessagesPlaceholder(variable_name="messages"),
            ]
        else:
            template = [
                SystemMessage(content=base_instructions),
                MessagesPlaceholder(variable_name="messages"),
            ]

        return ChatPromptTemplate.from_messages(template)

    async def replan_step(self, state: PlanAndExecuteAgentState, config: RunnableConfig):
        """根据执行结果重新规划步骤或生成最终响应

        Args:
            state: 当前状态
            config: 可运行配置

        Returns:
            包含新计划或最终响应的状态更新
        """
        messages = state['messages']

        user_message = config["configurable"]["graph_request"].user_message

        # 检查是否已经有响应
        if state.get("response"):
            self.log(config, f"已有最终响应，无需重新规划")
            return state

        # 格式化过去的步骤 - 改进格式以更清晰地显示执行结果
        past_steps_formatted = "\n".join([
            f"步骤 {i + 1}: {step[0]}\n执行结果: {step[1]}\n"
            for i, step in enumerate(state["past_steps"])
        ])

        # 检查是否所有步骤已完成
        all_steps_completed = len(state.get("plan", [])) == 0 and len(
            state.get("past_steps", [])) > 0

        # 创建提示模板
        replanner_prompt = self._create_planning_prompt(for_replanning=True)

        # 获取LLM客户端
        llm = self.get_llm_client(config["configurable"]["graph_request"])

        # 人类消息的内容根据是否完成所有步骤有所不同
        message_content = ""
        if all_steps_completed:
            message_content = f"""所有计划步骤已完成，请根据以下执行结果综合给出最终答案。

目标任务: {user_message}

详细执行步骤和结果:
{past_steps_formatted}

重要说明：
- 请仔细查看每个步骤的执行结果
- 如果执行结果包含了具体的数值、字符串或信息，请提取实际内容
- 不要将变量名当作最终结果
- 请基于实际的执行输出给出准确的最终答案

请直接提供最终的答案，无需创建新的计划。
"""
        else:
            message_content = f"请基于已完成的步骤重新评估计划，目标是：{user_message}"

        # 人类消息
        human_message = HumanMessage(content=message_content)
        messages.append(human_message)

        # 通用结构化输出调用，兼容 Qwen Function
        self.log(config,
                 f"执行{'最终结果整理' if all_steps_completed else '重新规划'}，已完成 {len(state['past_steps'])} 个步骤")
        output = await self.call_with_structured_output(
            llm=llm,
            prompt=replanner_prompt,
            pydantic_model=Act,
            messages=messages,
        )

        # 创建系统消息
        if isinstance(output.action, Response):
            self.log(config, f"重新规划结果：完成任务，返回最终响应")
            # 生成最终响应
            ai_message = AIMessage(
                content=f"任务已完成，最终结果：{output.action.response}")
            messages.append(ai_message)
            return {
                "messages": messages,
                "response": output.action.response
            }
        else:
            # 生成新计划
            new_plan = output.action.steps
            self.log(config, f"重新规划结果：新计划包含 {len(new_plan)} 个步骤")
            plan_str = "\n".join([f"- {step}" for step in new_plan])
            ai_message = AIMessage(content=f"已重新规划任务，新计划：\n{plan_str}")
            messages.append(ai_message)

            return {
                "messages": messages,
                "plan": new_plan,
                "current_step_index": 0
            }

    async def plan_step(self, state: PlanAndExecuteAgentState, config: RunnableConfig):
        """生成初始计划步骤

        Args:
            state: 当前状态
            config: 可运行配置

        Returns:
            包含初始计划的状态更新
        """
        messages = state['messages']

        # 获取用户消息
        user_message = config["configurable"]["graph_request"].user_message

        # 创建人类消息
        human_message = HumanMessage(content=user_message)

        # 创建提示模板
        planner_prompt = self._create_planning_prompt(for_replanning=False)

        # 获取LLM客户端
        llm = self.get_llm_client(config["configurable"]["graph_request"])

        # 通用结构化输出调用，兼容 Qwen Function
        self.log(config, f"为任务生成初始计划: {user_message}")
        plan = await self.call_with_structured_output(
            llm=llm,
            prompt=planner_prompt,
            pydantic_model=Plan,
            messages=[human_message,],
        )

        # 格式化计划
        plan_str = "\n".join([f"- {step}" for step in plan.steps])
        self.log(config, f"生成的初始计划包含 {len(plan.steps)} 个步骤")
        self.log(config, f"生成的初始计划:\n{plan_str}")

        # 创建系统消息和AI消息，以便将它们添加到状态
        ai_message = AIMessage(
            content=f"已为任务生成计划，包含 {len(plan.steps)} 个步骤:\n{plan_str}")
        messages.append(ai_message)

        # 返回更新的状态
        return {
            "messages": messages,
            "plan": plan.steps,
            "current_step_index": 0,
            "past_steps": []
        }
