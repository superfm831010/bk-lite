from sanic import Blueprint, json
from sanic_ext import validate
from src.core.sanic_plus.auth.api_auth import auth
from src.entity.rag.graphiti.index_delete_request import IndexDeleteRequest
from src.entity.rag.graphiti.document_delete_request import DocumentDeleteRequest
from src.entity.rag.graphiti.document_ingest_request import GraphitiRagDocumentIngestRequest
from src.entity.rag.graphiti.document_retriever_request import DocumentRetrieverRequest
from src.entity.rag.graphiti.rebuild_community_request import RebuildCommunityRequest
from src.rag.graph_rag.graphiti.graphiti_rag import GraphitiRAG

graph_rag_api_router = Blueprint(
    "graph_rag_api_router", url_prefix="/graph_rag")


@graph_rag_api_router.post("/ingest")
@auth.login_required
@validate(json=GraphitiRagDocumentIngestRequest)
async def ingest(request, body: GraphitiRagDocumentIngestRequest):
    rag = GraphitiRAG()
    rs = await rag.ingest(body)
    return json({"status": "success", "result": rs})


@graph_rag_api_router.post("/rebuild_community")
@auth.login_required
@validate(json=RebuildCommunityRequest)
async def rebuild_community(request, body: RebuildCommunityRequest):
    rag = GraphitiRAG()
    await rag.rebuild_community(body)
    return json({"status": "success"})


@graph_rag_api_router.post("/search")
@auth.login_required
@validate(json=DocumentRetrieverRequest)
async def search(request, body: DocumentRetrieverRequest):
    rag = GraphitiRAG()
    result = await rag.search(body)
    return json({"status": "success", "result": result})


@graph_rag_api_router.post("/list_index_documents")
@auth.login_required
@validate(json=DocumentRetrieverRequest)
async def list_index_documents(request, body: DocumentRetrieverRequest):
    rag = GraphitiRAG()
    result = await rag.list_index_document(body)
    return json({"status": "success", "result": result})


@graph_rag_api_router.post("/delete_document")
@auth.login_required
@validate(json=DocumentDeleteRequest)
async def delete_document(request, body: DocumentDeleteRequest):
    rag = GraphitiRAG()
    await rag.delete_document(body)
    return json({"status": "success"})


@graph_rag_api_router.post("/delete_index")
@auth.login_required
@validate(json=IndexDeleteRequest)
async def delete_index(request, body: IndexDeleteRequest):
    rag = GraphitiRAG()
    await rag.delete_index(body)
    return json({"status": "success"})
