from sanic import Blueprint, json
from sanic_ext import validate
from src.core.sanic_plus.auth.api_auth import auth
from src.web.entity.rag.graphiti.index_delete_request import IndexDeleteRequest
from src.web.entity.rag.graphiti.document_delete_request import DocumentDeleteRequest
from src.web.entity.rag.graphiti.document_ingest_request import GraphitiRagDocumentIngestRequest
from src.web.entity.rag.graphiti.document_retriever_request import DocumentRetrieverRequest
from src.web.entity.rag.graphiti.rebuild_community_request import RebuildCommunityRequest
from src.core.rag.graph_rag.graphiti.graphiti_rag import GraphitiRAG

graph_rag_api_router = Blueprint(
    "graph_rag_api_router", url_prefix="/graph_rag")


@graph_rag_api_router.post("/ingest")
@auth.login_required
@validate(json=GraphitiRagDocumentIngestRequest)
async def ingest(request, body: GraphitiRagDocumentIngestRequest):
    from sanic.log import logger
    import asyncio

    logger.info(f"接收到文档摄取请求: group_id={body.group_id}, 文档数量={len(body.docs)}")

    try:
        rag = GraphitiRAG()

        rs = await asyncio.wait_for(rag.ingest(body), timeout=60*60*24)
        logger.info(f"文档摄取请求完成: group_id={body.group_id}")
        return json({"status": "success", "result": rs})
    except asyncio.TimeoutError:
        logger.error(f"文档摄取超时: group_id={body.group_id}, 超时时间: 24小时")
        return json({
            "status": "error",
            "message": "文档摄取操作超时，请减少文档数量或联系管理员"
        }, status=408)
    except Exception as e:
        logger.error(f"文档摄取异常: group_id={body.group_id}, 错误: {e}")
        return json({
            "status": "error",
            "message": f"文档摄取失败: {str(e)}"
        }, status=500)


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
