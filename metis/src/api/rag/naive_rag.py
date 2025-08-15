import json as js
import tempfile
import time
import uuid

from sanic.log import logger
from sanic import Blueprint, json
from sanic_ext import validate

from src.core.sanic_plus.auth.api_auth import auth
from src.entity.rag.base.document_count_request import DocumentCountRequest
from src.entity.rag.base.document_delete_request import DocumentDeleteRequest
from src.entity.rag.base.document_list_request import DocumentListRequest
from src.entity.rag.base.document_metadata_update_request import DocumentMetadataUpdateRequest
from src.entity.rag.base.document_retriever_request import DocumentRetrieverRequest
from src.entity.rag.base.index_delete_request import IndexDeleteRequest
from src.loader.raw_loader import RawLoader
from src.loader.website_loader import WebSiteLoader
from src.rag.naive_rag.elasticsearch.elasticsearch_rag import ElasticSearchRag
from src.services.rag_service import RagService

naive_rag_api_router = Blueprint("naive_rag_api_router", url_prefix="/rag")


@naive_rag_api_router.post("/naive_rag_test")
@auth.login_required
@validate(json=DocumentRetrieverRequest)
def naive_rag_test(request, body: DocumentRetrieverRequest):
    rag = ElasticSearchRag()
    documents = rag.search(body)
    return json({
        "status": "success",
        "message": "",
        "documents": [doc.model_dump() for doc in documents]
    })


@naive_rag_api_router.post("/count_index_document")
@auth.login_required
@validate(json=DocumentCountRequest)
async def count_index_document(request, body: DocumentCountRequest):
    rag = ElasticSearchRag()
    count = rag.count_index_document(body)
    return json({"status": "success", "message": "", "count": count})


@naive_rag_api_router.post("/custom_content_ingest")
@auth.login_required
async def custom_content_ingest(request):
    content = request.form.get('content')
    chunk_mode = request.form.get('chunk_mode')
    is_preview = request.form.get('preview', 'false').lower() == 'true'
    metadata = js.loads(request.form.get('metadata', '{}'))

    # 加载自定义内容
    loader = RawLoader(content)
    docs = loader.load()

    # 处理文档元数据
    docs = RagService.prepare_documents_metadata(docs,
                                                 is_preview=is_preview,
                                                 title="自定义内容",
                                                 knowledge_id=request.form.get('knowledge_id'))
    # 执行文档分块
    chunker = RagService.get_chunker(chunk_mode, request)
    chunked_docs = chunker.chunk(docs)

    # 处理预览模式
    if is_preview:
        return json({
            "status": "success",
            "message": "",
            "documents": RagService.serialize_documents(chunked_docs),
            "chunks_size": len(chunked_docs)
        })

    # 执行文档存储
    logger.debug(f"开始存储{len(chunked_docs)}个文档分块，将自动添加created_time字段以支持时间排序")
    RagService.store_documents_to_es(
        chunked_docs=chunked_docs,
        knowledge_base_id=request.form.get('knowledge_base_id'),
        embed_model_base_url=request.form.get('embed_model_base_url'),
        embed_model_api_key=request.form.get('embed_model_api_key'),
        embed_model_name=request.form.get('embed_model_name'),
        metadata=metadata
    )
    return json({"status": "success", "message": "", "chunks_size": len(chunked_docs)})


@naive_rag_api_router.post("/website_ingest")
@auth.login_required
async def website_ingest(request):
    url = request.form.get('url')
    max_depth = int(request.form.get('max_depth', 1))
    chunk_mode = request.form.get('chunk_mode')
    is_preview = request.form.get('preview', 'false').lower() == 'true'
    metadata = js.loads(request.form.get('metadata', '{}'))

    loader = WebSiteLoader(url, max_depth)
    docs = loader.load()

    # 处理文档元数据
    docs = RagService.prepare_documents_metadata(docs,
                                                 is_preview=is_preview,
                                                 title=url,
                                                 knowledge_id=request.form.get('knowledge_id'))

    # 执行文档分块并记录日志
    chunked_docs = RagService.perform_chunking(
        docs, chunk_mode, request, is_preview, "网站内容")

    # 处理预览模式
    if is_preview:
        return json({
            "status": "success",
            "message": "",
            "documents": RagService.serialize_documents(chunked_docs),
            "chunks_size": len(chunked_docs)
        })

    # 执行文档存储
    logger.debug(f"开始存储网站内容{len(chunked_docs)}个文档分块，将自动添加created_time字段")
    RagService.store_documents_to_es(
        chunked_docs=chunked_docs,
        knowledge_base_id=request.form.get('knowledge_base_id'),
        embed_model_base_url=request.form.get('embed_model_base_url'),
        embed_model_api_key=request.form.get('embed_model_api_key'),
        embed_model_name=request.form.get('embed_model_name'),
        metadata=metadata
    )

    return json({"status": "success", "message": "", "chunks_size": len(chunked_docs)})


@naive_rag_api_router.post("/file_ingest")
@auth.login_required
async def file_ingest(request):
    file = request.files.get('file')
    allowed_types = ['docx', 'pptx', 'ppt', 'doc', 'txt',
                     'jpg', 'png', 'jpeg', 'pdf', 'csv', 'xlsx', 'xls', 'md']

    file_extension = file.name.split(
        '.')[-1].lower() if '.' in file.name else ''
    if file_extension not in allowed_types:
        return json({"status": "error", "message": f"不支持的文件类型。支持的类型: {', '.join(allowed_types)}"})

    is_preview = request.form.get('preview', 'false').lower() == 'true'
    chunk_mode = request.form.get('chunk_mode')
    metadata = js.loads(request.form.get('metadata', '{}'))
    load_mode = request.form.get('load_mode', 'full')

    with tempfile.NamedTemporaryFile(delete=True, suffix=f'.{file_extension}') as temp_file:
        temp_file.write(file.body)
        temp_file.flush()
        temp_path = temp_file.name

        # 加载文件内容
        loader = RagService.get_file_loader(
            temp_path, file_extension, load_mode, request)
        docs = loader.load()

        # 处理文档元数据
        docs = RagService.prepare_documents_metadata(docs,
                                                     is_preview=is_preview,
                                                     title=file.name,
                                                     knowledge_id=request.form.get('knowledge_id'))

        # 执行文档分块并记录日志
        chunked_docs = RagService.perform_chunking(
            docs, chunk_mode, request, is_preview, "文件内容")

        # 处理预览模式
        if is_preview:
            return json({
                "status": "success",
                "message": "",
                "documents": RagService.serialize_documents(chunked_docs),
                "chunks_size": len(chunked_docs)
            })

        # 执行文档存储
        logger.debug(f"开始存储文件内容{len(chunked_docs)}个文档分块，将自动添加created_time字段")
        RagService.store_documents_to_es(
            chunked_docs=chunked_docs,
            knowledge_base_id=request.form.get('knowledge_base_id'),
            embed_model_base_url=request.form.get('embed_model_base_url'),
            embed_model_api_key=request.form.get('embed_model_api_key'),
            embed_model_name=request.form.get('embed_model_name'),
            metadata=metadata
        )

    return json({"status": "success", "message": "", "chunks_size": len(chunked_docs)})


@naive_rag_api_router.post("/delete_index")
@validate(json=IndexDeleteRequest)
@auth.login_required
async def delete_index(request, body: IndexDeleteRequest):
    rag = ElasticSearchRag()
    rag.delete_index(body)
    return json({"status": "success", "message": ""})


@naive_rag_api_router.post("/delete_doc")
@auth.login_required
@validate(json=DocumentDeleteRequest)
async def delete_doc(request, body: DocumentDeleteRequest):
    rag = ElasticSearchRag()
    rag.delete_document(body)
    return json({"status": "success", "message": ""})


@naive_rag_api_router.post("/list_rag_document")
@auth.login_required
@validate(json=DocumentListRequest)
async def list_rag_document(request, body: DocumentListRequest):
    rag = ElasticSearchRag()

    # 记录排序字段，用于向后兼容性检查
    logger.debug(f"查询文档列表，排序字段: {body.sort_field}, 排序方式: {body.sort_order}")
    if 'created_time' in body.sort_field:
        logger.debug("使用时间字段排序，已启用向后兼容性处理")

    documents = rag.list_index_document(body)
    return json({"status": "success", "message": "", "documents": [doc.dict() for doc in documents]})


@naive_rag_api_router.post("/update_rag_document_metadata")
@auth.login_required
@validate(json=DocumentMetadataUpdateRequest)
async def update_rag_document_metadata(request, body: DocumentMetadataUpdateRequest):
    rag = ElasticSearchRag()
    rag.update_metadata(body)
    return json({"status": "success", "message": "文档元数据更新成功"})
