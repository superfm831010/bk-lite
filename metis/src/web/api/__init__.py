from sanic import Blueprint

from src.web.api.agent.chatbot_workflow.chatbot_workflow import chatbot_workflow_api_router
from src.web.api.agent.lats_agent.lats_agent import lats_agent_router
from src.web.api.agent.plan_and_execute_agent.plan_and_execute_agent import plan_and_execute_agent_router
from src.web.api.agent.react_agent.react_agent import react_agent_api_router
from src.web.api.rag.naive_rag import naive_rag_api_router
from src.web.api.rag.graph_rag import graph_rag_api_router
from src.web.api.rag.rag_enhance import rag_enhance_api_router

BLUEPRINTS = []

# Agent Routers
BLUEPRINTS += [chatbot_workflow_api_router, react_agent_api_router,
               lats_agent_router,
               plan_and_execute_agent_router]

# RAG Routers
BLUEPRINTS += [naive_rag_api_router,
               rag_enhance_api_router, graph_rag_api_router]


api = Blueprint.group(*BLUEPRINTS, url_prefix="/api")
