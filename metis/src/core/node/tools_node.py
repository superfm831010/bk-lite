from langchain_mcp_adapters.client import MultiServerMCPClient
from sanic.log import logger
from src.core.node.structured_output_parser import StructuredOutputParser
from src.tools.tools_loader import ToolsLoader
from src.core.node.basic_node import BasicNode
from typing import Dict, List, Union
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel


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
