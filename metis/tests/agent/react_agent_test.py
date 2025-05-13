import os
from typing import List

import pytest
from langchain_core.messages import AIMessageChunk
from loguru import logger

from src.core.entity.tools_server import ToolsServer
from src.entity.agent.react_agent_request import ReActAgentRequest
from src.agent.react_agent.react_agent_graph import ReActAgentGraph


@pytest.mark.asyncio
async def test_react_agent_with_time_tools():
    tools_servers: List[ToolsServer] = [
        ToolsServer(name="time", url='langchain:current_time'),
        ToolsServer(name="duckduckgo", url='langchain:duckduckgo'),
    ]

    request = ReActAgentRequest(
        model="gpt-4o",
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        user_message="现在几点",
        user_id="umr",
        thread_id="2",
        tools_servers=tools_servers,
    )
    graph = ReActAgentGraph()

    logger.info(f"messages 模式")
    result = await graph.stream(request)
    await graph.aprint_chunk(result)
    print('\n')

    logger.info(f"values模式")
    result = await graph.execute(request)
    logger.info(result)
    print('\n')


@pytest.mark.asyncio
async def test_react_agent_with_jenkins_tools():
    tools_servers: List[ToolsServer] = [
        ToolsServer(name="jenkins", url='langchain:jenkins'),
        # MCPServer(name="time mcp", url="http://127.0.0.1:17000/sse"),
    ]

    msgs = [
        "Jenkins有多少个构建任务,最新一次构建成功的任务是哪个",
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
