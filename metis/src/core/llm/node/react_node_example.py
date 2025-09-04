"""
ReAct 节点组合的使用示例

展示如何在不同的场景中复用 ReAct 节点组合
"""
from langgraph.constants import END
from langgraph.graph import StateGraph
from typing import Dict, Any
from langchain_core.runnables import RunnableConfig

from src.core.llm.node.tools_node import ToolsNodes
from src.core.agent.react_agent.react_agent_state import ReActAgentState


class ExampleReActUsage(ToolsNodes):
    """展示如何复用 ReAct 节点组合的示例类"""

    async def example_multi_react_graph(self, request):
        """
        示例：在一个图中使用多个 ReAct 节点组合

        这展示了如何在复杂的工作流中组合多个 ReAct 模式
        """
        await self.setup(request)

        # 创建状态图
        graph_builder = StateGraph(ReActAgentState)

        # 添加初始处理节点
        async def initial_processing(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
            self.log(config, "开始初始处理")
            return state

        graph_builder.add_node("initial", initial_processing)

        # 第一个 ReAct 组合：数据收集阶段
        data_collection_entry, _ = self.build_react_nodes(
            graph_builder=graph_builder,
            llm_node_name="data_collector_llm",
            tool_node_name="data_collector_tools",
            system_prompt="你是一个数据收集专家，专门负责收集和整理信息。",
            end_node="analysis_phase",  # 完成后进入分析阶段
            tools_node=None
        )

        # 分析阶段节点
        async def analysis_phase(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
            self.log(config, "进入分析阶段")
            return state

        graph_builder.add_node("analysis_phase", analysis_phase)

        # 第二个 ReAct 组合：分析处理阶段
        analysis_entry, _ = self.build_react_nodes(
            graph_builder=graph_builder,
            llm_node_name="analyzer_llm",
            tool_node_name="analyzer_tools",
            system_prompt="你是一个数据分析专家，专门负责分析和推理。",
            end_node=END,  # 完成后结束
            tools_node=None
        )

        # 构建执行流程
        graph_builder.set_entry_point("initial")
        graph_builder.add_edge("initial", data_collection_entry)
        graph_builder.add_edge("analysis_phase", analysis_entry)

        return graph_builder.compile()

    async def example_custom_end_node(self, request):
        """
        示例：自定义结束节点的 ReAct 组合

        展示如何将 ReAct 组合集成到更大的工作流中
        """
        await self.setup(request)

        # 创建状态图
        graph_builder = StateGraph(ReActAgentState)

        # 自定义结束处理节点
        async def custom_end_processing(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
            self.log(config, "执行自定义结束处理")
            # 这里可以添加特殊的后处理逻辑
            return state

        graph_builder.add_node("custom_end", custom_end_processing)

        # 使用自定义结束节点的 ReAct 组合
        react_entry, _ = self.build_react_nodes(
            graph_builder=graph_builder,
            llm_node_name="main_llm",
            tool_node_name="main_tools",
            system_prompt="你是一个通用助手，完成任务后需要进行特殊的后处理。",
            end_node="custom_end",  # 使用自定义结束节点
            tools_node=None
        )

        # 自定义结束节点完成后才真正结束
        graph_builder.add_edge("custom_end", END)

        # 设置入口点
        graph_builder.set_entry_point(react_entry)

        return graph_builder.compile()

    async def example_external_tools(self, request, external_tools_node):
        """
        示例：使用外部工具节点的 ReAct 组合

        展示如何传入外部构建的工具节点
        """
        await self.setup(request)

        # 创建状态图
        graph_builder = StateGraph(ReActAgentState)

        # 使用外部传入的工具节点
        react_entry, _ = self.build_react_nodes(
            graph_builder=graph_builder,
            llm_node_name="external_tools_llm",
            tool_node_name="external_tools_node",
            system_prompt="你是一个使用外部工具的专家助手。",
            end_node=END,
            tools_node=external_tools_node  # 使用外部工具节点
        )

        # 设置入口点
        graph_builder.set_entry_point(react_entry)

        return graph_builder.compile()


# 使用示例的函数
async def create_simple_react_graph(request):
    """创建一个简单的 ReAct 图的便捷函数"""
    builder = ExampleReActUsage()
    await builder.setup(request)

    graph_builder = StateGraph(ReActAgentState)

    # 使用默认配置创建 ReAct 组合
    react_entry, _ = builder.build_react_nodes(
        graph_builder=graph_builder,
        system_prompt="你是一个智能助手。"
    )

    graph_builder.set_entry_point(react_entry)
    return graph_builder.compile()
