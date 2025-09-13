from langchain_mcp_adapters.client import MultiServerMCPClient
from sanic.log import logger
from src.core.llm.node.structured_output_parser import StructuredOutputParser
from src.core.tools.tools_loader import ToolsLoader
from src.core.llm.node.basic_node import BasicNode
from typing import Dict, List, Union, Literal, Optional, Any, Callable
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph
from langgraph.constants import END
from pydantic import BaseModel
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dataclasses import dataclass


class ToolsNodes(BasicNode):
    def __init__(self) -> None:
        self.tools = []
        self.mcp_client = None
        self.mcp_config = {}
        self.tools_prompt_tokens = 0
        self.tools_completions_tokens = 0

    async def call_with_structured_output(self, llm, prompt, pydantic_model,
                                          messages: Union[Dict, List], max_retries: int = 3):
        """
        通用结构化输出调用方法

        Args:
            llm: LangChain LLM实例
            prompt: LangChain prompt模板
            pydantic_model: 目标Pydantic模型类
            messages: 消息内容 (dict或list格式)
            max_retries: 最大重试次数

        Returns:
            解析后的Pydantic模型实例
        """
        parser = StructuredOutputParser(llm, max_retries=max_retries)
        return await parser.parse_with_structured_output(prompt, messages, pydantic_model)

    async def setup(self, request: BaseModel):
        """初始化工具节点"""
        # 初始化MCP客户端配置
        for server in request.tools_servers:
            if not server.url.startswith("langchain:"):
                self.mcp_config[server.name] = {
                    "url": server.url,
                    "transport": 'sse'
                }

        if self.mcp_config:
            self.mcp_client = MultiServerMCPClient(self.mcp_config)
            self.tools = await self.mcp_client.get_tools()

        # 初始化LangChain工具
        for server in request.tools_servers:
            if server.url.startswith("langchain:"):
                langchain_tools = ToolsLoader.load_tools(server)
                self.tools.extend(langchain_tools)

    async def build_tools_node(self) -> ToolNode:
        """构建工具节点"""
        try:
            if self.tools:
                tool_node = ToolNode(self.tools, handle_tool_errors=True)
                logger.info(f"成功构建工具节点，包含 {len(self.tools)} 个工具")
                return tool_node
            else:
                logger.info("未找到可用工具，返回空工具节点")
                return ToolNode([])
        except Exception as e:
            logger.error(f"构建工具节点失败: {e}")
            return ToolNode([])

    # ========== 简化的 ReAct 节点组合构建器 ==========

    def build_react_nodes(self,
                          graph_builder: StateGraph,
                          composite_node_name: str = "react_agent",
                          system_prompt: Optional[str] = None,
                          end_node: str = END,
                          tools_node: Optional[ToolNode] = None,
                          max_iterations: int = 10) -> str:
        """
        构建独立闭环的 ReAct Agent 组合节点

        这是一个可复用的组合节点，Agent 负责执行工具，有解决方案就结束，
        没有解决方案就继续循环，直到达到最大迭代次数。

        Args:
            graph_builder: StateGraph 构建器
            composite_node_name: 组合节点名称
            system_prompt: 系统提示
            end_node: 结束节点  
            tools_node: 外部工具节点
            max_iterations: 最大迭代次数

        Returns:
            str: 组合节点的出口节点名称
        """
        # 内部节点名称
        llm_node_name = f"{composite_node_name}_llm"
        tool_node_name = f"{composite_node_name}_tools"

        # 添加 LLM 节点
        async def llm_node(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
            try:
                messages = state["messages"]
                graph_request = config["configurable"]["graph_request"]

                # 获取 LLM 并绑定工具
                llm = self.get_llm_client(graph_request).bind_tools(self.tools)

                # 构建提示 - 使用现有的模板系统
                if system_prompt:
                    # 使用传入的自定义系统提示
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        MessagesPlaceholder(variable_name="messages"),
                    ])
                else:
                    # 使用现有的基础模板系统
                    from src.core.sanic_plus.utils.template_loader import TemplateLoader
                    system_message_prompt = TemplateLoader.render_template(
                        'prompts/graph/base_node_system_message', {
                            "user_system_message": getattr(graph_request, 'system_message_prompt', "你是一个智能助手，能够使用工具来帮助问题。请仔细分析问题，使用合适的工具获取信息，并在找到解决方案后给出最终答案。")
                        })
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", system_message_prompt),
                        MessagesPlaceholder(variable_name="messages"),
                    ])

                # 调用 LLM
                response = await (prompt | llm).ainvoke({"messages": messages})

                # 更新迭代计数
                current_iteration = state.get("react_iteration", 0) + 1
                return {
                    "messages": [response],
                    "react_iteration": current_iteration
                }

            except Exception as e:
                logger.error(f"ReAct LLM 节点失败: {e}")
                return {"messages": [AIMessage(content=f"处理失败: {str(e)}")]}

        graph_builder.add_node(llm_node_name, llm_node)

        # 添加工具节点
        async def tool_node(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
            try:
                current_tools_node = tools_node or await self.build_tools_node()
                return await current_tools_node.ainvoke(state)
            except Exception as e:
                logger.error(f"ReAct 工具节点失败: {e}")
                return {"messages": [ToolMessage(content=f"工具执行失败: {str(e)}", tool_call_id="error")]}

        graph_builder.add_node(tool_node_name, tool_node)

        # 条件判断函数 - 决定是否继续循环或结束
        def should_continue(state: Dict[str, Any]) -> Literal["tools", "end"]:
            messages = state.get("messages", [])
            current_iteration = state.get("react_iteration", 0)

            # 检查是否达到最大迭代次数
            if current_iteration >= max_iterations:
                logger.warning(f"ReAct Agent 达到最大迭代次数 {max_iterations}，强制结束")
                return "end"

            # 检查最后一条消息是否有工具调用
            if messages and hasattr(messages[-1], 'tool_calls') and messages[-1].tool_calls:
                return "tools"

            # 没有工具调用，表示 Agent 认为已经有了解决方案
            return "end"

        # 添加条件边和回环边
        graph_builder.add_conditional_edges(
            llm_node_name,
            should_continue,
            {"tools": tool_node_name, "end": end_node}
        )
        # 工具执行后回到 LLM 继续思考
        graph_builder.add_edge(tool_node_name, llm_node_name)

        return llm_node_name  # 返回组合节点的入口节点
