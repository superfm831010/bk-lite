from src.entity.agent.react_agent.react_agent_request import ReActAgentRequest
from src.core.entity.tools_server import ToolsServer
from src.agent.react_agent.react_agent_graph import ReActAgentGraph
import os
from typing import List

import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_react_agent_with_time_tools():
    tools_servers: List[ToolsServer] = [
        ToolsServer(name="current_time", url='langchain:current_time'),
        ToolsServer(name="jenkins", url='langchain:jenkins'),
        ToolsServer(name="python_analyze_repl",
                    url='langchain:python_analyze_repl'),
        ToolsServer(name="duckduckgo", url='langchain:duckduckgo'),
    ]

    request = ReActAgentRequest(
        model="gpt-4o",
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        user_message="把现在的时间，转换成字符串，然后在字符串的前面加上'hello world'，最后返回这个字符串",
        user_id="umr",
        thread_id="2",
        tools_servers=tools_servers,
    )
    graph = ReActAgentGraph()

    logger.info(f"values模式")
    result = graph.execute(request)
    logger.info(result)

    logger.info(f"messages 模式")
    result = await graph.stream(request)
    await graph.aprint_chunk(result)
    print('\n')


@pytest.mark.asyncio
async def test_react_agent_with_jenkins_tools():
    tools_servers: List[ToolsServer] = [
        ToolsServer(name="jenkins", url='langchain:jenkins'),
    ]

    msgs = [
        "Jenkins有多少个构建任务",
    ]
    for m in msgs:
        request = ReActAgentRequest(
            model="gpt-4o",
            openai_api_base=os.getenv("OPENAI_BASE_URL"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            user_message=m,
            user_id="umr",
            thread_id="2",
            tools_servers=tools_servers,
            extra_config={
                "jenkins_url": os.getenv("TEST_JENKINS_URL"),
                "jenkins_username": os.getenv("TEST_JENKINS_USERNAME"),
                "jenkins_password": os.getenv("TEST_JENKINS_PASSWORD"),
            }
        )
        graph = ReActAgentGraph()
        result = await graph.execute(request)
        logger.info(result)


#
# @pytest.mark.asyncio
# async def test_react_agent_with_ansible_tools():
#     tools_servers: List[ToolsServer] = [
#         ToolsServer(name="ansible_adhoc", url='langchain:ansible', extra_prompt={}),
#     ]
#
#     request = ReActAgentRequest(
#         model="gpt-4o",
#         openai_api_base=os.getenv("OPENAI_BASE_URL"),
#         openai_api_key=os.getenv("OPENAI_API_KEY"),
#         user_message="mysql有几张库",
#         user_id="umr",
#         thread_id="2",
#         tools_servers=tools_servers,
#         extra_config={
#             "module": "mysql_info",
#             "module_args": "login_user=root login_host=127.0.0.1 login_password=123456",
#         }
#     )
#     graph = ReActAgentGraph()
#
#     logger.info(f"messages 模式")
#     result = await graph.stream(request)
#     await graph.aprint_chunk(result)
#     print('\n')


@pytest.mark.asyncio
async def test_react_agent_with_ansible_inventory_tools():
    tools_servers: List[ToolsServer] = [
        ToolsServer(name="ansible_adhoc", url='langchain:ansible',
                    extra_param_prompt={}, extra_tools_prompt='这个工具可以获取主机名称'),
    ]

    request = ReActAgentRequest(
        model="gpt-4o",
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        user_message="这些机器的主机名",
        user_id="umr",
        thread_id="2",
        tools_servers=tools_servers,
        extra_config={
            # "inventory": os.getenv("TEST_ANSIBLE_INVENTORY"),
            "module": "command",
            "module_args": "hostname",
        }
    )
    graph = ReActAgentGraph()

    logger.info(f"messages 模式")
    result = await graph.stream(request)
    await graph.aprint_chunk(result)
    print('\n')


# @pytest.mark.asyncio
# async def test_react_agent_with_http_request_tools():
#     tools_servers: List[ToolsServer] = [
#         ToolsServer(name="http_request", url='langchain:http_request', extra_prompt={
#             "limit": "这个可以限制取多少条数据",
#         }),
#     ]

#     request = ReActAgentRequest(
#         model="gpt-4o",
#         openai_api_base=os.getenv("OPENAI_BASE_URL"),
#         openai_api_key=os.getenv("OPENAI_API_KEY"),
#         user_message="热门电影前十展示",
#         user_id="umr",
#         thread_id="2",
#         tools_servers=tools_servers,
#         extra_config={
#             "url": "https://m.douban.com/rexxar/api/v2/subject/recent_hot/movie?limit={{limit}}",
#             "headers": '{"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36","referer":"https://movie.douban.com/","Origin":"https://movie.douban.com"}',
#         }
#     )
#     graph = ReActAgentGraph()

#     logger.info(f"messages 模式")
#     result = await graph.stream(request)
#     await graph.aprint_chunk(result)
#     print('\n')
