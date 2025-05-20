import os
from typing import List

import pytest

from src.agent.plan_and_execute_agent.plan_and_execute_agent_graph import PlanAndExecuteAgentGraph
from src.core.entity.tools_server import ToolsServer
from src.entity.agent.plan_and_execute_agent.plan_and_execute_agent_request import PlanAndExecuteAgentRequest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_compile_graph():
    tools_servers: List[ToolsServer] = [
        ToolsServer(name="current_time", url='langchain:current_time'),
        ToolsServer(name="jenkins", url='langchain:jenkins'),
        ToolsServer(name="python_analyze_repl", url='langchain:python_analyze_repl'),
    ]

    request = PlanAndExecuteAgentRequest(
        model="gpt-4o",
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        user_message="明天是星期几",
        user_id="umr",
        thread_id="2",
        tools_servers=tools_servers,
        extra_config={
            "jenkins_url": os.getenv("TEST_JENKINS_URL"),
            "jenkins_username": os.getenv("TEST_JENKINS_USERNAME"),
            "jenkins_password": os.getenv("TEST_JENKINS_PASSWORD"),
        }
    )
    graph = PlanAndExecuteAgentGraph()

    logger.info(f"messages 模式")
    result = await graph.stream(request)
    await graph.aprint_chunk(result)
    print('\n')
