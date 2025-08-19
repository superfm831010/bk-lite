from src.core.llm.entity.basic_llm_request import BasicLLMRequest
from src.core.llm.graph.basic_graph import BasicGraph


from src.core.tools.playwright_tools import cleanup_playwright


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
        if hasattr(request, 'tools_servers'):
            for server in getattr(request, 'tools_servers', []):
                if 'local:playwright_tools' in getattr(server, 'url', ''):
                    await cleanup_playwright()
                    return
