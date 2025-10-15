import time
from typing import TypedDict, Annotated, List, Optional

from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.constants import END
from langgraph.graph import StateGraph, add_messages
from pydantic import BaseModel, Field
from loguru import logger

from neco.llm.chain.entity import BasicLLMRequest, BasicLLMResponse, ToolsServer
from neco.llm.chain.graph import BasicGraph
from neco.llm.chain.node import ToolsNodes

class PlanAndExecuteAgentResponse(BasicLLMResponse):
    pass

class PlanAndExecuteAgentRequest(BasicLLMRequest):
    tools_servers: List[ToolsServer] = []
    langchain_tools: List[str] = []

class PlanAndExecuteAgentState(TypedDict):
    """真正的Plan and Execute Agent状态管理"""
    messages: Annotated[List[BaseMessage], add_messages]
    graph_request: PlanAndExecuteAgentRequest
    
    # 计划相关
    original_plan: List[str]      # 原始计划
    current_plan: List[str]       # 当前剩余步骤
    
    # 执行相关
    execution_prompt: Optional[str]  # 当前步骤的执行提示
    
    # 最终结果
    final_response: Optional[str]

class Plan(BaseModel):
    """动态计划模型"""
    steps: List[str] = Field(description="当前剩余的执行步骤列表，每个步骤应该具体明确且可执行")

class PlanResponse(BaseModel):
    """计划响应模型"""
    plan: Plan = Field(description="生成的执行计划")
    reasoning: str = Field(description="计划制定的推理过程")

class ReplanResponse(BaseModel):
    """重新规划响应模型"""
    updated_plan: Plan = Field(description="更新后的剩余步骤")
    reasoning: str = Field(description="重新规划的推理过程")
    is_complete: bool = Field(description="任务是否已经完成，无需继续执行")

class PlanAndExecuteAgentNode(ToolsNodes):
    """Plan and Execute Agent - 智能计划生成与执行"""

    async def planner_node(self, state: PlanAndExecuteAgentState, config: RunnableConfig):
        """动态计划生成节点 - 真正的Plan and Execute Agent"""
        
        user_message = config["configurable"]["graph_request"].user_message
        
        # 获取可用工具信息
        tools_info = ""
        if hasattr(self, 'tools') and self.tools:
            tools_list = []
            for tool in self.tools:
                tool_name = getattr(tool, 'name', str(tool))
                tool_desc = getattr(tool, 'description', '工具功能')
                tools_list.append(f"  • {tool_name}: {tool_desc}")
            
            tools_info = f"""

🔧 **可用工具**:
{chr(10).join(tools_list)}"""
        
        # 动态计划生成提示
        planning_prompt = f"""你是一个智能任务规划师。请为以下任务制定详细的执行计划。

📋 **用户任务**: {user_message}{tools_info}

🎯 **规划指南**:
1. 分析任务的具体需求和目标
2. 识别需要使用的工具和资源  
3. 制定清晰、可执行的步骤序列
4. 每个步骤都应该是具体的行动项
5. 充分利用可用工具的能力

请提供你的推理过程和具体的执行计划。"""

        try:
            # 使用LLM动态生成计划
            plan_response = await self.structured_output_parser.parse_with_structured_output(
                user_message=planning_prompt,
                pydantic_class=PlanResponse
            )
            
            plan_steps = plan_response.plan.steps
            reasoning = plan_response.reasoning
            
        except Exception as e:
            logger.warning(f"动态计划生成失败: {e}")
            # 紧急备用计划
            plan_steps = ["分析用户需求", "执行必要的操作", "提供结果"]
            reasoning = "使用备用计划"
        
        # 显示规划过程
        steps_display = "\n".join([f"   {i+1}. {step}" for i, step in enumerate(plan_steps)])
        
        plan_display = f"""🎯 **任务规划完成**

📋 **执行计划**:
{steps_display}

🚀 **开始执行...**"""
        
        self.log(config, plan_display)
        
        return {
            "messages": [AIMessage(content=plan_display)],
            "original_plan": plan_steps,
            "current_plan": plan_steps,
            "final_response": None
        }

    async def executor_node(self, state: PlanAndExecuteAgentState, config: RunnableConfig):
        """单步执行节点 - 执行当前计划的第一步"""
        
        current_plan = state.get("current_plan", [])
        if not current_plan:
            # 没有待执行步骤，直接进入总结
            return {**state, "final_response": "所有步骤已完成"}
        
        current_step = current_plan[0]  # 取第一个待执行步骤
        
        step_display = f"""⚡ **执行**: {current_step}"""
        
        self.log(config, step_display)
        
        # 使用ReAct模式执行当前步骤
        execution_prompt = f"""请执行以下具体步骤：

🎯 **当前步骤**: {current_step}

📋 **原始任务**: {config["configurable"]["graph_request"].user_message}

请专注于完成这一个步骤，使用必要的工具，并提供执行结果。"""
        
        # 传递执行提示给React节点使用
        return {
            **state,
            "messages": state.get("messages", []) + [AIMessage(content=step_display)],
            "execution_prompt": execution_prompt
        }

    async def replanner_node(self, state: PlanAndExecuteAgentState, config: RunnableConfig):
        """重新规划节点 - 根据执行结果动态调整计划"""
        
        current_plan = state.get("current_plan", [])
        messages = state.get("messages", [])
        
        if not current_plan:
            return {**state, "final_response": "计划执行完成"}
        
        # 获取最近的执行结果
        recent_results = []
        for msg in messages[-3:]:  # 检查最近3条消息
            if hasattr(msg, 'content') and msg.content:
                recent_results.append(msg.content)
        
        execution_context = "\n".join(recent_results) if recent_results else "暂无执行结果"
        completed_step = current_plan[0] if current_plan else "无"
        remaining_steps = current_plan[1:] if len(current_plan) > 1 else []
        
        # 重新规划提示
        replan_prompt = f"""基于当前执行情况，请重新评估和调整执行计划。

📋 **原始任务**: {config["configurable"]["graph_request"].user_message}

✅ **已完成步骤**: {completed_step}

📊 **执行结果**: 
{execution_context}

📝 **剩余原计划**: {remaining_steps}

🤔 **重新规划要求**:
1. 分析当前执行结果是否符合预期
2. 评估是否需要调整剩余步骤
3. 如果任务已基本完成，可以标记为完成
4. 如果需要继续，请调整优化剩余步骤

请提供重新规划的分析和调整后的步骤。"""

        try:
            replan_response = await self.structured_output_parser.parse_with_structured_output(
                user_message=replan_prompt,
                pydantic_class=ReplanResponse
            )
            
            if replan_response.is_complete:
                # 任务完成
                replan_display = f"""✅ **任务完成**: {replan_response.reasoning}"""
                
                return {
                    **state,
                    "messages": state.get("messages", []) + [AIMessage(content=replan_display)],
                    "current_plan": [],
                    "final_response": "任务执行完成"
                }
            else:
                # 更新计划继续执行
                new_steps = replan_response.updated_plan.steps
                replan_display = f"""🔄 **计划调整**: 剩余 {len(new_steps)} 个步骤

📋 **接下来**:
{chr(10).join([f"   {i+1}. {step}" for i, step in enumerate(new_steps)])}"""
                
                self.log(config, replan_display)
                
                return {
                    **state,
                    "messages": state.get("messages", []) + [AIMessage(content=replan_display)],
                    "current_plan": new_steps
                }
        
        except Exception as e:
            logger.warning(f"重新规划失败: {e}")
            # 简单移除已完成的步骤
            remaining = current_plan[1:] if len(current_plan) > 1 else []
            return {
                **state,
                "current_plan": remaining
            }

    async def should_continue(self, state: PlanAndExecuteAgentState) -> str:
        """判断是否继续执行或结束"""
        current_plan = state.get("current_plan", [])
        final_response = state.get("final_response")
        
        # 如果有明确的最终响应或没有剩余步骤，结束执行
        if final_response or not current_plan:
            return "summary"
        
        # 否则继续执行
        return "executor"

    async def summary_node(self, state: PlanAndExecuteAgentState, config: RunnableConfig):
        """最终总结节点"""
        
        # 从消息中提取最终答案
        messages = state.get("messages", [])
        final_answer = ""
        
        # 找到最后的有效AI消息作为最终结果  
        for message in reversed(messages):
            if (hasattr(message, 'content') and message.content and 
                not any(starter in message.content for starter in ["🎯 **智能任务规划**", "⚡ **执行步骤**", "🔄 **计划调整**"])):
                final_answer = message.content
                break
        
        if not final_answer:
            final_answer = "任务已完成"
        
        # 获取执行统计
        original_plan = state.get("original_plan", [])
        total_steps = len(original_plan)
        
        # 创建最终总结 - 简化版本，避免重复显示结果
        summary = f"""✅ **任务完成** ({total_steps} 个步骤已执行)

{final_answer}"""

        self.log(config, summary)
        
        return {
            **state,
            "messages": state.get("messages", []) + [AIMessage(content=summary)],
            "final_response": final_answer
        }

class PlanAndExecuteAgentGraph(BasicGraph):
    """Plan and Execute Agent - 智能计划生成与执行系统"""

    async def compile_graph(self, request: PlanAndExecuteAgentRequest):
        """编译工作流图"""
        node_builder = PlanAndExecuteAgentNode()
        logger.debug("🚀 初始化Plan and Execute Agent")
        await node_builder.setup(request)
        logger.debug(f"🔧 已加载 {len(node_builder.tools)} 个工具")

        graph_builder = StateGraph(PlanAndExecuteAgentState)
        last_edge = self.prepare_graph(graph_builder, node_builder)

        # 添加核心节点
        graph_builder.add_node("planner", node_builder.planner_node)
        graph_builder.add_node("executor", node_builder.executor_node)  
        graph_builder.add_node("replanner", node_builder.replanner_node)
        graph_builder.add_node("summary", node_builder.summary_node)
        
        # 添加动态步骤执行包装节点
        async def step_executor_wrapper(state: PlanAndExecuteAgentState, config: RunnableConfig):
            """包装节点：动态设置执行步骤提示"""
            execution_prompt = state.get("execution_prompt", "请完成当前任务")
            
            # 直接传递执行提示给React节点，不显示额外的状态信息
            current_step_msg = HumanMessage(content=execution_prompt)
            
            return {
                **state,
                "messages": state.get("messages", []) + [current_step_msg]
            }
        
        graph_builder.add_node("step_executor_wrapper", step_executor_wrapper)
        
        # 使用现有的ReAct节点构建方法，传入步骤执行的系统提示
        react_entry_node = await node_builder.build_react_nodes(
            graph_builder=graph_builder,
            composite_node_name="react_step_executor", 
            additional_system_prompt="你是任务执行助手，专注完成用户最新消息中的具体步骤。请使用合适的工具完成任务，并简洁地提供结果。",
            next_node="replanner"  # 执行完单步后进行重新规划
        )

        # 设置图边缘 - 实现 Plan -> Execute -> Replan -> Execute 循环
        graph_builder.add_edge(last_edge, "planner")                    # 开始 -> 计划
        graph_builder.add_edge("planner", "executor")                   # 计划 -> 准备执行
        graph_builder.add_edge("executor", "step_executor_wrapper")     # 准备执行 -> 步骤包装
        graph_builder.add_edge("step_executor_wrapper", react_entry_node)  # 步骤包装 -> React执行
        # react_step_executor 自动连接到 replanner
        
        # 条件边：重新规划后决定继续执行还是结束
        graph_builder.add_conditional_edges(
            "replanner",
            node_builder.should_continue,
            {
                "executor": "executor",   # 继续执行下一步
                "summary": "summary"      # 任务完成，生成总结
            }
        )
        
        graph_builder.add_edge("summary", END)

        logger.debug("✅ Plan and Execute Agent编译完成")
        
        graph = graph_builder.compile()
        return graph