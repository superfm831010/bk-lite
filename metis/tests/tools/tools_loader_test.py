"""
tools_loader.py 的单元测试

测试插件化工具加载器的功能：
- 工具发现功能
- 工具加载功能
- enable_extra_prompt 配置功能
"""

from src.core.entity.tools_server import ToolsServer
from src.tools.tools_loader import ToolsLoader
import pytest
from pathlib import Path
import sys

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def test_discover_tools():
    """测试工具发现功能"""
    tools_map = ToolsLoader._discover_tools()

    # 验证基本功能
    assert isinstance(tools_map, dict)
    assert len(tools_map) > 0, "应该发现至少一个工具类别"

    # 验证预期的工具类别（基于实际包含工具的文件）
    # 只验证实际包含工具的类别
    expected_categories = ['time', 'http_request', 'kubernetes', 'jenkins',
                           'ansible', 'python', 'search']
    for category in expected_categories:
        assert category in tools_map, f"应该发现 {category} 工具类别"

    # 验证工具结构
    for category, tools in tools_map.items():
        assert isinstance(tools, list), f"{category} 应该是工具列表"
        assert len(tools) > 0, f"{category} 应该包含至少一个工具"

        for tool in tools:
            assert 'func' in tool, "工具应该包含 func 字段"
            assert 'enable_extra_prompt' in tool, "工具应该包含 enable_extra_prompt 字段"
            assert isinstance(
                tool['enable_extra_prompt'], bool), "enable_extra_prompt 应该是布尔值"


def test_tools_extra_prompt_enabled():
    """测试 _tools_plus.py 文件的工具启用额外提示功能"""
    tools_map = ToolsLoader._discover_tools()

    # 验证从 _tools_plus.py 文件加载的工具启用了额外提示
    # 注意：ansible 和 http_request 现在来自 _tools_plus.py 文件
    plus_categories = ['http_request', 'ansible']  # 这些实际来自 _tools_plus.py 文件

    for category in plus_categories:
        if category in tools_map:
            tools = tools_map[category]
            for tool in tools:
                assert tool['enable_extra_prompt'], f"{category} 工具 {tool['func'].name} 应该启用额外提示"


def test_tools_extra_prompt_disabled():
    """测试 _tools.py 文件的工具不启用额外提示功能"""
    tools_map = ToolsLoader._discover_tools()

    # 验证从 _tools.py 文件加载的工具不启用额外提示
    # 注意：ansible 和 http_request 现在来自 _tools_plus.py 文件，所以不在这个列表中
    # playwright 文件是空的，也不会出现在 tools_map 中
    regular_categories = ['time', 'kubernetes', 'jenkins', 'python', 'search']

    for category in regular_categories:
        if category in tools_map:
            tools = tools_map[category]
            for tool in tools:
                assert not tool['enable_extra_prompt'], f"{category} 工具 {tool['func'].name} 不应该启用额外提示"


def test_file_naming_convention():
    """测试文件命名约定对 enable_extra_prompt 的影响"""
    tools_map = ToolsLoader._discover_tools()

    # 基于实际的文件结构进行测试
    for category, tools in tools_map.items():
        for tool in tools:
            if category in ['http_request', 'ansible']:
                # 这些来自 _tools_plus.py 文件，应该启用额外提示
                assert tool['enable_extra_prompt'], f"来自 _tools_plus.py 的 {category} 工具应该启用额外提示"
            else:
                # 这些来自 _tools.py 文件，不应该启用额外提示
                assert not tool['enable_extra_prompt'], f"来自 _tools.py 的 {category} 工具不应该启用额外提示"


def test_load_tools_time_category():
    """测试加载时间工具"""
    time_server = ToolsServer(
        name="time_server",
        url="langchain:time"
    )

    tools = ToolsLoader.load_tools(time_server)

    assert isinstance(tools, list)
    assert len(tools) == 1, "时间类别应该有 1 个工具"
    assert tools[0].name == "get_current_time"


def test_load_tools_http_request_category():
    """测试加载 HTTP 请求工具 (现在来自 _tools_plus.py 版本)"""
    http_server = ToolsServer(
        name="http_server",
        url="langchain:http_request",
        extra_tools_prompt="这是测试的额外提示",
        extra_param_prompt={"url": "API端点", "method": "HTTP方法"}
    )

    tools = ToolsLoader.load_tools(http_server)

    assert isinstance(tools, list)
    assert len(tools) == 4, "HTTP 类别应该有 4 个工具"

    # 验证工具名称
    tool_names = {tool.name for tool in tools}
    expected_names = {'http_get', 'http_post', 'http_put', 'http_delete'}
    assert tool_names == expected_names

    # 验证额外提示被添加（因为现在这是来自 _tools_plus.py 文件）
    for tool in tools:
        assert "这是测试的额外提示" in tool.description
        assert "以下是函数的动态参数生成要求" in tool.description


def test_load_tools_invalid_category():
    """测试加载不存在的工具类别"""
    invalid_server = ToolsServer(
        name="invalid_server",
        url="langchain:non_existent"
    )

    tools = ToolsLoader.load_tools(invalid_server)

    assert isinstance(tools, list)
    assert len(tools) == 0, "不存在的类别应该返回空列表"


def test_tool_category_naming():
    """测试工具类别命名规则"""
    tools_map = ToolsLoader._discover_tools()

    # 验证类别名称符合预期格式
    for category in tools_map.keys():
        # 所有类别名称不应该包含 _tools 或 _tools_plus
        assert "_tools" not in category, f"类别名 {category} 不应该包含 _tools"
        assert isinstance(category, str)
        assert len(category) > 0


def test_tool_functions_valid():
    """测试工具函数的有效性"""
    tools_map = ToolsLoader._discover_tools()

    for category, tools in tools_map.items():
        for tool in tools:
            func = tool['func']

            # 验证工具函数有必要的属性
            assert hasattr(func, 'name'), f"{category} 工具应该有 name 属性"
            assert hasattr(
                func, 'description'), f"{category} 工具应该有 description 属性"
            assert isinstance(func.name, str)
            assert isinstance(func.description, str)
            assert len(func.name) > 0
            assert len(func.description) > 10


def test_load_tools_preserves_original():
    """测试工具加载不会修改原始工具"""
    # 先获取原始工具
    tools_map = ToolsLoader._discover_tools()

    # 测试普通工具（不应该被修改）
    if 'time' in tools_map:
        original_desc = tools_map['time'][0]['func'].description

        # 加载工具
        time_server = ToolsServer(
            name="time_server",
            url="langchain:time",
            extra_tools_prompt="测试提示",
            extra_param_prompt={"test": "测试参数"}
        )

        loaded_tools = ToolsLoader.load_tools(time_server)

        # 再次获取工具映射，验证原始描述未被修改
        tools_map_after = ToolsLoader._discover_tools()
        if 'time' in tools_map_after:
            after_desc = tools_map_after['time'][0]['func'].description
            assert original_desc == after_desc, "原始工具描述不应该被修改"

    # 测试 plus 工具（描述会被修改，但原始工具不应该受影响）
    if 'http_request' in tools_map:
        original_plus_desc = tools_map['http_request'][0]['func'].description

        # 加载 plus 工具
        http_server = ToolsServer(
            name="http_server",
            url="langchain:http_request",
            extra_tools_prompt="测试提示",
            extra_param_prompt={"test": "测试参数"}
        )

        loaded_plus_tools = ToolsLoader.load_tools(http_server)

        # 验证加载的工具描述被修改了
        if loaded_plus_tools:
            loaded_desc = loaded_plus_tools[0].description
            assert "测试提示" in loaded_desc, "加载的工具描述应该包含额外提示"

        # 再次获取工具映射，验证原始描述未被修改
        tools_map_after = ToolsLoader._discover_tools()
        if 'http_request' in tools_map_after:
            after_plus_desc = tools_map_after['http_request'][0]['func'].description
            assert original_plus_desc == after_plus_desc, "原始 plus 工具描述不应该被修改"


def test_discover_tools_categorization():
    """测试工具发现和分类功能"""
    tools_map = ToolsLoader._discover_tools()

    # 验证普通工具和 plus 工具被正确分类
    regular_tools = []
    plus_tools = []

    for category, tools in tools_map.items():
        if category in ['http_request', 'ansible']:
            # 这些来自 _tools_plus.py 文件
            plus_tools.extend(tools)
            # 验证 plus 工具启用额外提示
            for tool in tools:
                assert tool['enable_extra_prompt'], f"{category} 中的工具应该启用额外提示"
        else:
            # 这些来自 _tools.py 文件
            regular_tools.extend(tools)
            # 验证普通工具不启用额外提示
            for tool in tools:
                assert not tool['enable_extra_prompt'], f"{category} 中的工具不应该启用额外提示"

    # 验证至少找到了一些工具
    assert len(regular_tools) > 0, "应该发现一些普通工具"
    assert len(plus_tools) > 0, "应该发现一些 plus 工具"

    print(f"发现 {len(regular_tools)} 个普通工具，{len(plus_tools)} 个 plus 工具")


# pytest fixtures
@pytest.fixture
def sample_tools_map():
    """提供示例工具映射用于测试"""
    return ToolsLoader._discover_tools()


@pytest.fixture
def time_server():
    """提供时间服务器配置用于测试"""
    return ToolsServer(
        name="time_server",
        url="langchain:time"
    )


@pytest.fixture
def http_server():
    """提供HTTP服务器配置用于测试"""
    return ToolsServer(
        name="http_server",
        url="langchain:http_request",
        extra_tools_prompt="测试额外提示",
        extra_param_prompt={"url": "API端点", "method": "HTTP方法"}
    )
