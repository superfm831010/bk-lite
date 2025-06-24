from regex import B
from sanic import Blueprint

from src.api.agent.chatbot_workflow import chatbot_workflow_api_router
from src.api.agent.react_agent import react_agent_api_router
from src.api.rag.naive_rag import naive_rag_api_router
from src.api.mlops.anomaly_detection_api import anomaly_detection_api_router
from src.api.rag.rag_enhance import rag_enhance_api_router

BLUEPRINTS = []

# Agnet Routers
BLUEPRINTS += [chatbot_workflow_api_router, react_agent_api_router]

# RAG Routers
BLUEPRINTS += [naive_rag_api_router, rag_enhance_api_router]

# MLOPS Routers
BLUEPRINTS += [anomaly_detection_api_router]

api = Blueprint.group(*BLUEPRINTS, url_prefix="/api")
