import json as js
import tempfile
import time
import traceback
import uuid

from loguru import logger
from sanic import Blueprint, json
from sanic_ext import validate

from src.core.web.api_auth import auth
from src.enhance.qa_enhance import QAEnhance
from src.entity.rag.elasticsearch_document_count_request import ElasticSearchDocumentCountRequest
from src.entity.rag.elasticsearch_document_delete_request import ElasticSearchDocumentDeleteRequest
from src.entity.rag.elasticsearch_document_list_request import ElasticSearchDocumentListRequest
from src.entity.rag.elasticsearch_document_metadata_update_request import \
    ElasticsearchDocumentMetadataUpdateRequest
from src.entity.rag.elasticsearch_index_delete_request import ElasticSearchIndexDeleteRequest
from src.entity.rag.elasticsearch_retriever_request import ElasticSearchRetrieverRequest
from src.entity.rag.qa_enhance_request import QAEnhanceRequest
from src.entity.rag.summarize_enhance_request import SummarizeEnhanceRequest
from src.loader.raw_loader import RawLoader
from src.loader.website_loader import WebSiteLoader
from src.rag.native_rag.elasticsearch_rag import ElasticSearchRag
from src.services.rag_service import RagService
from src.summarize.summarize_manager import SummarizeManager

rag_api_router = Blueprint("rag", url_prefix="/rag")


@rag_api_router.post("/naive_rag_test")
@auth.login_required
@validate(json=ElasticSearchRetrieverRequest)
def naive_rag_test(request, body: ElasticSearchRetrieverRequest):
    """
    测试RAG
    :param request:
    :param body:
    :return:
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] RAG测试请求开始, 参数: {body.dict()}")
    try:
        rag = ElasticSearchRag()
        documents = rag.search(body)
        logger.info(
            f"[{request_id}] RAG测试请求成功, 耗时: {time.time() - start_time:.2f}秒, 返回文档数: {len(documents)}")
        return json({"status": "success", "message": "", "documents": [doc.dict() for doc in documents]})
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"[{request_id}] RAG测试请求失败: {str(e)}\n{error_detail}")
        return json({"status": "error", "message": str(e)})


@rag_api_router.post("/count_index_document")
@auth.login_required
@validate(json=ElasticSearchDocumentCountRequest)
async def count_index_document(request, body: ElasticSearchDocumentCountRequest):
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] 计数索引文档请求, 索引: {body.index_name}")
    try:
        rag = ElasticSearchRag()
        count = rag.count_index_document(body)
        logger.info(f"[{request_id}] 计数索引文档请求成功, 文档数: {count}")
        return json({"status": "success", "message": "", "count": count})
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"[{request_id}] 计数索引文档请求失败: {str(e)}\n{error_detail}")
        return json({"status": "error", "message": str(e)})


@rag_api_router.post("/summarize_enhance")
@auth.login_required
@validate(json=SummarizeEnhanceRequest)
async def summarize_enhance(request, body: SummarizeEnhanceRequest):
    """
    文本摘要增强
    :param request:
    :param body:
    :return:
    """
    """
    文本摘要增强
    :param request:
    :param body:
    :return:
    """
    result = SummarizeManager.summarize(body.content, body.model, body.openai_api_base, body.openai_api_key)
    return json({"status": "success", "message": result})


@rag_api_router.post("/qa_pair_generate")
@auth.login_required
@validate(json=QAEnhanceRequest)
async def qa_pair_generate(request, body: QAEnhanceRequest):
    """
    QA 问答对生成
    :param request:
    :return:
    """
    """
    生成问答对
    :param request:
    :return:
    """
    qa_enhance = QAEnhance(body)
    result = qa_enhance.generate_qa()
    return json({"status": "success", "message": result})


@rag_api_router.post("/custom_content_ingest")
@auth.login_required
async def custom_content_ingest(request):
    start_time = time.time()
    request_id = str(uuid.uuid4())[:8]
    knowledge_id = request.form.get('knowledge_id', 'unknown')
    knowledge_base_id = request.form.get('knowledge_base_id', 'unknown')
    logger.info(f"[{request_id}] 自定义内容导入请求开始, 知识库ID: {knowledge_base_id}, 知识ID: {knowledge_id}")

    try:
        content = request.form.get('content')
        content_preview = content[:100] + '...' if len(content) > 100 else content
        chunk_mode = request.form.get('chunk_mode')
        is_preview = request.form.get('preview', 'false').lower() == 'true'
        metadata = js.loads(request.form.get('metadata', '{}'))

        logger.debug(f"[{request_id}] 内容预览: {content_preview}, 分块模式: {chunk_mode}, 预览模式: {is_preview}")

        # 加载自定义内容
        loader = RawLoader(content)
        docs = loader.load()
        logger.debug(f"[{request_id}] 加载内容完成, 文档数: {len(docs)}")

        # 处理文档元数据
        docs = RagService.prepare_documents_metadata(docs,
                                                     is_preview=is_preview,
                                                     title="自定义内容",
                                                     knowledge_id=request.form.get('knowledge_id'))
        # 执行文档分块
        chunker = RagService.get_chunker(chunk_mode, request)
        chunking_start_time = time.time()
        chunked_docs = chunker.chunk(docs)

        logger.debug(
            f"[{request_id}] 分块完成, 耗时: {time.time() - chunking_start_time:.2f}秒, 分块数: {len(chunked_docs)}")

        # 处理预览模式
        if is_preview:
            response_time = time.time() - start_time
            logger.info(
                f"[{request_id}] 自定义内容预览完成, 总耗时: {response_time:.2f}秒, 分块数: {len(chunked_docs)}")
            return json({
                "status": "success",
                "message": "",
                "documents": RagService.serialize_documents(chunked_docs),
                "chunks_size": len(chunked_docs)
            })

        # 执行文档存储
        embedding_start_time = time.time()
        RagService.store_documents_to_es(
            chunked_docs=chunked_docs,
            knowledge_base_id=request.form.get('knowledge_base_id'),
            embed_model_base_url=request.form.get('embed_model_base_url'),
            embed_model_api_key=request.form.get('embed_model_api_key'),
            embed_model_name=request.form.get('embed_model_name'),
            metadata=metadata
        )
        logger.debug(f"[{request_id}] 存储到ES完成, 嵌入耗时: {time.time() - embedding_start_time:.2f}秒")

        response_time = time.time() - start_time
        logger.info(
            f"[{request_id}] 自定义内容导入请求完成, 总耗时: {response_time:.2f}秒, 分块数: {len(chunked_docs)}")
        return json({"status": "success", "message": "", "chunks_size": len(chunked_docs)})
    except Exception as e:
        error_detail = traceback.format_exc()
        response_time = time.time() - start_time
        logger.error(f"[{request_id}] 自定义内容处理错误, 耗时: {response_time:.2f}秒, 错误: {str(e)}\n{error_detail}")
        return json({"status": "error", "message": str(e)})


@rag_api_router.post("/website_ingest")
@auth.login_required
async def website_ingest(request):
    start_time = time.time()
    request_id = str(uuid.uuid4())[:8]
    knowledge_id = request.form.get('knowledge_id', 'unknown')
    knowledge_base_id = request.form.get('knowledge_base_id', 'unknown')

    try:
        url = request.form.get('url')
        max_depth = int(request.form.get('max_depth', 1))
        chunk_mode = request.form.get('chunk_mode')
        is_preview = request.form.get('preview', 'false').lower() == 'true'
        metadata = js.loads(request.form.get('metadata', '{}'))

        logger.info(
            f"[{request_id}] 网站内容导入请求开始, 知识库ID: {knowledge_base_id}, 知识ID: {knowledge_id}, URL: {url}, 最大深度: {max_depth}")

        # 加载网站内容
        loading_start_time = time.time()
        loader = WebSiteLoader(url, max_depth)
        docs = loader.load()
        logger.debug(
            f"[{request_id}] 网站内容加载完成, 耗时: {time.time() - loading_start_time:.2f}秒, 文档数: {len(docs)}")

        # 处理文档元数据
        docs = RagService.prepare_documents_metadata(docs,
                                                     is_preview=is_preview,
                                                     title=url,
                                                     knowledge_id=request.form.get('knowledge_id'))

        # 执行文档分块并记录日志
        chunking_start_time = time.time()
        chunked_docs = RagService.perform_chunking(
            docs, chunk_mode, request, is_preview, "网站内容")
        logger.debug(
            f"[{request_id}] 网站内容分块完成, 耗时: {time.time() - chunking_start_time:.2f}秒, 分块数: {len(chunked_docs)}")

        # 处理预览模式
        if is_preview:
            response_time = time.time() - start_time
            logger.info(f"[{request_id}] 网站内容预览完成, 总耗时: {response_time:.2f}秒, 分块数: {len(chunked_docs)}")
            return json({
                "status": "success",
                "message": "",
                "documents": RagService.serialize_documents(chunked_docs),
                "chunks_size": len(chunked_docs)
            })

        # 执行文档存储
        embedding_start_time = time.time()
        RagService.store_documents_to_es(
            chunked_docs=chunked_docs,
            knowledge_base_id=request.form.get('knowledge_base_id'),
            embed_model_base_url=request.form.get('embed_model_base_url'),
            embed_model_api_key=request.form.get('embed_model_api_key'),
            embed_model_name=request.form.get('embed_model_name'),
            metadata=metadata
        )
        logger.debug(f"[{request_id}] 网站内容存储到ES完成, 嵌入耗时: {time.time() - embedding_start_time:.2f}秒")

        response_time = time.time() - start_time
        logger.info(f"[{request_id}] 网站内容导入请求完成, 总耗时: {response_time:.2f}秒, 分块数: {len(chunked_docs)}")
        return json({"status": "success", "message": "", "chunks_size": len(chunked_docs)})
    except Exception as e:
        error_detail = traceback.format_exc()
        response_time = time.time() - start_time
        logger.error(f"[{request_id}] 网站内容处理错误, 耗时: {response_time:.2f}秒, 错误: {str(e)}\n{error_detail}")
        return json({"status": "error", "message": str(e)})


@rag_api_router.post("/file_ingest")
@auth.login_required
async def file_ingest(request):
    start_time = time.time()
    request_id = str(uuid.uuid4())[:8]

    file = request.files.get('file')
    file_size_mb = len(file.body) / (1024 * 1024)
    knowledge_id = request.form.get('knowledge_id', 'unknown')
    knowledge_base_id = request.form.get('knowledge_base_id', 'unknown')

    logger.info(
        f"[{request_id}] 文件导入请求开始, 知识库ID: {knowledge_base_id}, 知识ID: {knowledge_id}, 文件名: {file.name}, 文件大小: {file_size_mb:.2f} MB")

    allowed_types = ['docx', 'pptx', 'ppt', 'doc', 'txt',
                     'jpg', 'png', 'jpeg', 'pdf', 'csv', 'xlsx', 'xls', 'md']
    file_extension = file.name.split(
        '.')[-1].lower() if '.' in file.name else ''

    if file_extension not in allowed_types:
        logger.warn(f"[{request_id}] 不支持的文件类型: {file_extension}")
        return json({"status": "error", "message": f"不支持的文件类型。支持的类型: {', '.join(allowed_types)}"})

    is_preview = request.form.get('preview', 'false').lower() == 'true'
    chunk_mode = request.form.get('chunk_mode')
    metadata = js.loads(request.form.get('metadata', '{}'))
    load_mode = request.form.get('load_mode', 'full')

    logger.debug(f"[{request_id}] 文件处理模式: 分块模式={chunk_mode}, 预览模式={is_preview}")

    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=f'.{file_extension}') as temp_file:
            temp_file.write(file.body)
            temp_file.flush()
            temp_path = temp_file.name

            # 日志记录
            operation_type = "预览分块文件" if is_preview else "处理文件"
            logger.debug(f'[{request_id}] {operation_type}：{temp_path}')

            # 加载文件内容
            loading_start_time = time.time()
            loader = RagService.get_file_loader(temp_path, file_extension, load_mode, request)
            docs = loader.load()
            logger.debug(
                f"[{request_id}] 文件内容加载完成, 耗时: {time.time() - loading_start_time:.2f}秒, 文档数: {len(docs)}")

            # 处理文档元数据
            docs = RagService.prepare_documents_metadata(docs,
                                                         is_preview=is_preview,
                                                         title=file.name,
                                                         knowledge_id=request.form.get('knowledge_id'))

            # 执行文档分块并记录日志
            chunking_start_time = time.time()
            chunked_docs = RagService.perform_chunking(
                docs, chunk_mode, request, is_preview, "文件内容")
            logger.debug(
                f"[{request_id}] 文件内容分块完成, 耗时: {time.time() - chunking_start_time:.2f}秒, 分块数: {len(chunked_docs)}")

            # 处理预览模式
            if is_preview:
                response_time = time.time() - start_time
                logger.info(
                    f"[{request_id}] 文件内容预览完成, 总耗时: {response_time:.2f}秒, 分块数: {len(chunked_docs)}")
                return json({
                    "status": "success",
                    "message": "",
                    "documents": RagService.serialize_documents(chunked_docs),
                    "chunks_size": len(chunked_docs)
                })

            # 执行文档存储
            embedding_start_time = time.time()
            RagService.store_documents_to_es(
                chunked_docs=chunked_docs,
                knowledge_base_id=request.form.get('knowledge_base_id'),
                embed_model_base_url=request.form.get('embed_model_base_url'),
                embed_model_api_key=request.form.get('embed_model_api_key'),
                embed_model_name=request.form.get('embed_model_name'),
                metadata=metadata
            )
            logger.debug(f"[{request_id}] 文件内容存储到ES完成, 嵌入耗时: {time.time() - embedding_start_time:.2f}秒")

        response_time = time.time() - start_time
        logger.info(f"[{request_id}] 文件导入请求完成, 总耗时: {response_time:.2f}秒, 分块数: {len(chunked_docs)}")
        return json({"status": "success", "message": "", "chunks_size": len(chunked_docs)})
    except Exception as e:
        error_detail = traceback.format_exc()
        response_time = time.time() - start_time
        logger.error(f"[{request_id}] 文件处理错误, 耗时: {response_time:.2f}秒, 错误: {str(e)}\n{error_detail}")
        return json({"status": "error", "message": str(e)})


@rag_api_router.post("/delete_index")
@validate(json=ElasticSearchIndexDeleteRequest)
@auth.login_required
async def delete_index(request, body: ElasticSearchIndexDeleteRequest):
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] 删除索引请求, 索引名: {body.index_name}")
    try:
        rag = ElasticSearchRag()
        start_time = time.time()
        rag.delete_index(body)
        elapsed_time = time.time() - start_time
        logger.info(f"[{request_id}] 删除索引成功, 耗时: {elapsed_time:.2f}秒")
        return json({"status": "success", "message": ""})
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"[{request_id}] 删除索引失败: {str(e)}\n{error_detail}")
        return json({"status": "error", "message": str(e)})


@rag_api_router.post("/delete_doc")
@auth.login_required
@validate(json=ElasticSearchDocumentDeleteRequest)
async def delete_doc(request, body: ElasticSearchDocumentDeleteRequest):
    """
    删除文档
    :param request:
    :param body:
    :return:
    """
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] 删除文档请求, 索引名: {body.index_name}, 过滤条件: {body.metadata_filter}")
    try:
        start_time = time.time()
        rag = ElasticSearchRag()
        rag.delete_document(body)
        elapsed_time = time.time() - start_time
        logger.info(f"[{request_id}] 删除文档成功, 耗时: {elapsed_time:.2f}秒")
        return json({"status": "success", "message": ""})
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"[{request_id}] 删除文档失败: {str(e)}\n{error_detail}")
        return json({"status": "error", "message": str(e)})


@rag_api_router.post("/list_rag_document")
@auth.login_required
@validate(json=ElasticSearchDocumentListRequest)
async def list_rag_document(request, body: ElasticSearchDocumentListRequest):
    """
    查询RAG数据
    :param request:
    :param body:
    :return:
    """
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] 查询RAG文档列表请求, 索引名: {body.index_name}")
    try:
        start_time = time.time()
        rag = ElasticSearchRag()
        documents = rag.list_index_document(body)
        elapsed_time = time.time() - start_time
        logger.info(f"[{request_id}] 查询RAG文档列表成功, 耗时: {elapsed_time:.2f}秒, 文档数: {len(documents)}")
        return json({"status": "success", "message": "", "documents": [doc.dict() for doc in documents]})
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"[{request_id}] 查询RAG文档列表失败: {str(e)}\n{error_detail}")
        return json({"status": "error", "message": str(e)})


@rag_api_router.post("/update_rag_document_metadata")
@auth.login_required
@validate(json=ElasticsearchDocumentMetadataUpdateRequest)
async def update_rag_document_metadata(request, body: ElasticsearchDocumentMetadataUpdateRequest):
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] 更新文档元数据请求, 索引名: {body.index_name}, 过滤条件: {body.metadata_filter}")
    try:
        start_time = time.time()
        rag = ElasticSearchRag()
        rag.update_metadata(body)
        elapsed_time = time.time() - start_time
        logger.info(f"[{request_id}] 更新文档元数据成功, 耗时: {elapsed_time:.2f}秒")
        return json({"status": "success", "message": "文档元数据更新成功"})
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(f"[{request_id}] 更新文档元数据失败: {str(e)}\n{error_detail}")
        return json({"status": "error", "message": str(e)})
