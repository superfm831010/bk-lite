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
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


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

    # ========== 可复用的 ReAct 节点组合构建器 ==========

    def build_react_nodes(self,
                          graph_builder: StateGraph,
                          llm_node_name: str = "llm",
                          tool_node_name: str = "tools",
                          system_prompt: Optional[str] = None,
                          end_node: str = END,
                          tools_node: Optional[ToolNode] = None) -> tuple[str, Callable]:
        """
        构建可复用的 ReAct 节点组合

        Args:
            graph_builder: StateGraph 构建器
            llm_node_name: LLM 节点名称
            tool_node_name: 工具节点名称  
            system_prompt: 自定义系统提示，如果为 None 则使用默认 ReAct 提示
            end_node: LLM 节点的结束节点，默认为 END
            tools_node: 可选的外部工具节点，如果为 None 则使用内部构建的

        Returns:
            tuple[str, Callable]: (入口节点名称, 条件判断函数)
        """
        # 创建 LLM 节点函数
        async def llm_node_func(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
            return await self._react_llm_node_impl(state, config, system_prompt)

        # 创建工具节点函数
        async def tool_node_func(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
            # 如果没有提供外部工具节点，则使用内部构建的
            current_tools_node = tools_node if tools_node is not None else await self.build_tools_node()
            return await self._react_tool_node_impl(state, config, current_tools_node)

        # 创建条件判断函数
        def should_continue_func(state: Dict[str, Any]) -> Literal["tools", "end"]:
            return self._react_should_continue_impl(state, tool_node_name, end_node)

        # 添加节点到图
        graph_builder.add_node(llm_node_name, llm_node_func)
        graph_builder.add_node(tool_node_name, tool_node_func)

        # 添加条件边：LLM -> 工具 或 结束
        graph_builder.add_conditional_edges(
            llm_node_name,
            should_continue_func,
            {
                "tools": tool_node_name,
                "end": end_node
            }
        )

        # 工具执行后返回 LLM 继续推理
        graph_builder.add_edge(tool_node_name, llm_node_name)

        logger.info(
            f"✅ ReAct 节点组合构建完成: {llm_node_name} <-> {tool_node_name} -> {end_node}")

        return llm_node_name, should_continue_func

    async def _react_llm_node_impl(self, state: Dict[str, Any], config: RunnableConfig,
                                   system_message: Optional[str] = None) -> Dict[str, Any]:
        """ReAct LLM 推理节点实现"""
        messages = state["messages"]
        graph_request = config["configurable"]["graph_request"]

        self.log(config, f"开始执行 ReAct LLM 节点：输入消息数量: {len(messages)}")

        # 获取 LLM 客户端并绑定工具
        llm = self.get_llm_client(graph_request)
        llm_with_tools = llm.bind_tools(self.tools)

        # 构建提示模板
        prompt = self._build_react_prompt(
            system_message or getattr(
                graph_request, 'system_message_prompt', None)
        )

        # 创建处理链
        chain = prompt | llm_with_tools

        # 调用 LLM
        try:
            response: BaseMessage = await chain.ainvoke({
                "messages": messages
            })

            logger.info(
                f"ReAct LLM 生成响应，是否包含工具调用: {bool(getattr(response, 'tool_calls', None))}")

            return {
                "messages": [response]
            }

        except Exception as e:
            logger.error(f"ReAct LLM 节点执行失败: {e}")
            error_response = AIMessage(
                content=f"抱歉，处理您的请求时遇到了问题：{str(e)}"
            )
            return {
                "messages": [error_response]
            }

    async def _react_tool_node_impl(self, state: Dict[str, Any], config: RunnableConfig,
                                    tools_node: ToolNode) -> Dict[str, Any]:
        """ReAct 工具执行节点实现"""
        self.log(config, f"开始执行 ReAct 工具节点：当前消息数量: {len(state['messages'])}")

        try:
            # 使用传入的 ToolNode 执行工具
            result = await tools_node.ainvoke(state)

            # 记录工具执行结果
            tool_messages = result.get("messages", [])
            logger.info(f"ReAct 工具执行完成，生成 {len(tool_messages)} 条消息")

            return result

        except Exception as e:
            logger.error(f"ReAct 工具节点执行失败: {e}")
            # 返回错误消息
            from langchain_core.messages import ToolMessage
            error_message = ToolMessage(
                content=f"工具执行失败: {str(e)}",
                tool_call_id="error"
            )
            return {
                "messages": [error_message]
            }

    def _react_should_continue_impl(self, state: Dict[str, Any],
                                    tool_node_name: str, end_node: str) -> str:
        """ReAct 条件判断节点实现"""
        messages = state["messages"]
        if not messages:
            return end_node

        last_message = messages[-1]

        # 检查最后一条消息是否包含工具调用
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            logger.info(f"检测到工具调用，继续执行工具: {len(last_message.tool_calls)} 个")
            return "tools"  # 返回固定的 "tools"，在 build_react_nodes 中映射到实际节点名

        logger.info("无工具调用，结束执行")
        return "end"  # 返回固定的 "end"，在 build_react_nodes 中映射到实际结束节点

    def _build_react_prompt(self, system_message: str = None) -> ChatPromptTemplate:
        """构建 ReAct 风格的提示模板"""
        default_system = """你是一个智能助手，能够使用工具来帮助用户解决问题。

请遵循以下 ReAct (Reasoning and Acting) 模式：
1. 仔细分析用户的问题
2. 如果需要外部信息或执行特定操作，选择合适的工具
3. 根据工具的执行结果继续推理
4. 提供准确、有用的最终答案

可用工具说明：
- 仔细阅读每个工具的描述和参数要求
- 只在确实需要时调用工具
- 如果工具调用失败，尝试其他方法或提供基于现有信息的答案

请始终保持专业、准确和有帮助。"""

        system_prompt = system_message if system_message else default_system

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
