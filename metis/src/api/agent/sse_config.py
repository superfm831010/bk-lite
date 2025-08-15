"""
Plan and Execute Agent SSE 配置

管理 SSE 流式输出的各种配置选项
"""
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SSEDisplayConfig:
    """SSE 显示配置"""

    # 是否显示详细的工具执行信息
    show_tool_details: bool = True

    # 是否显示步骤进度
    show_progress: bool = True

    # 是否显示执行时间
    show_timing: bool = True

    # 工具结果摘要的最大长度
    tool_result_max_length: int = 200

    # 是否启用表情符号
    enable_emojis: bool = True

    # 自定义阶段显示文本
    phase_texts: Dict[str, str] = None

    # 工具名称映射
    tool_display_names: Dict[str, str] = None

    def __post_init__(self):
        """初始化后处理"""
        if self.phase_texts is None:
            self.phase_texts = {
                "initializing": "🎯 正在深入分析您的问题...",
                "planning": "📋 制定详细执行策略...",
                "executing": "⚡ 执行任务步骤",
                "tool_calling": "🔧 调用专业工具",
                "replanning": "🔄 智能调整策略",
                "finalizing": "✨ 精心整理最终答案...",
                "completed": "🎉 任务圆满完成！"
            }

        if self.tool_display_names is None:
            self.tool_display_names = {
                "naive_rag_search": "🔍 智能知识库搜索",
                "web_search": "🌐 网络信息搜索",
                "playwright_tools": "🎭 网页自动化操作",
                "python_repl": "🐍 Python 代码执行",
                "file_reader": "📄 文件内容读取",
                "calculator": "🔢 数学计算器",
                "code_executor": "💻 代码执行引擎",
                "document_processor": "📊 文档智能处理",
                "image_analyzer": "🖼️ 图像深度分析",
                "data_analyzer": "📈 数据专业分析",
                "search_tool": "🔍 搜索工具",
                "analysis_tool": "📊 分析工具",
                "processing_tool": "⚙️ 处理工具"
            }


# 默认配置
DEFAULT_SSE_CONFIG = SSEDisplayConfig()

# 简洁模式配置（减少冗余信息）
MINIMAL_SSE_CONFIG = SSEDisplayConfig(
    show_tool_details=False,
    show_timing=False,
    tool_result_max_length=100,
    enable_emojis=False,
    phase_texts={
        "initializing": "分析问题中...",
        "planning": "制定计划...",
        "executing": "执行中",
        "tool_calling": "调用工具",
        "replanning": "调整计划",
        "finalizing": "生成答案...",
        "completed": "完成"
    }
)

# 详细模式配置（显示更多信息）
VERBOSE_SSE_CONFIG = SSEDisplayConfig(
    show_tool_details=True,
    show_progress=True,
    show_timing=True,
    tool_result_max_length=500,
    enable_emojis=True
)
