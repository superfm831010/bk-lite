import os
import traceback
import uuid

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.constants import END
from langgraph.graph import MessagesState

from src.core.entity.basic_llm_request import BasicLLMRequest
from src.core.graph.basic_graph import BasicGraph


from src.tools.playwright_tools import cleanup_playwright


class ToolsGraph(BasicGraph):
    async def execute(self, request: BasicLLMRequest):
        # 执行主流程
        result = await super().execute(request)
        await self._cleanup_playwright_if_needed(request)
        return result

    async def stream(self, request: BasicLLMRequest):
        # 执行流式流程，包装生成器，消费完后再清理资源
        agen = await super().stream(request)

        async def _gen():
            try:
                async for item in agen:
                    yield item
            finally:
                await self._cleanup_playwright_if_needed(request)
        return _gen()

    async def _cleanup_playwright_if_needed(self, request):
        """
        检查 tools 列表是否包含 playwright 工具，若有则清理资源
        """
        # 兼容 node/tools_node 的 tools 列表
        tools = []
        if hasattr(request, 'tools_servers'):
            for server in getattr(request, 'tools_servers', []):
                # 只要有 playwright 字样就触发清理
                if 'playwright' in getattr(server, 'url', ''):
                    await cleanup_playwright()
                    return
        # 兜底：如果 tools 字段有 playwright 工具名
        if hasattr(request, 'tools'):
            for tool in getattr(request, 'tools', []):
                if hasattr(tool, 'name') and 'playwright' in tool.name:
                    await cleanup_playwright()
                    return
