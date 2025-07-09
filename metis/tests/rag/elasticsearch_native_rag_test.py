from src.rag.naive_rag.elasticsearch.elasticsearch_rag import ElasticSearchRag
from src.entity.rag.base.index_delete_request import IndexDeleteRequest
from src.entity.rag.base.document_retriever_request import DocumentRetrieverRequest
from src.entity.rag.base.document_metadata_update_request import DocumentMetadataUpdateRequest
from src.entity.rag.base.document_ingest_request import DocumentIngestRequest
from src.entity.rag.base.document_delete_request import DocumentDeleteRequest
import os
import uuid

from langchain_core.documents import Document

import logging

logger = logging.getLogger(__name__)


def get_sample_request(index_name=''):
    request = DocumentIngestRequest(
        index_name=index_name,
        index_mode='overwrite',
        docs=[
            Document(page_content='你好', metadata={
                'knowledge_title': '你好', 'knowledge_id': "1"}),
            Document(page_content='介绍一下你自己', metadata={
                'knowledge_title': '介绍一下你自己', 'knowledge_id': "2"}),
            Document(page_content='你是谁', metadata={
                'knowledge_title': '你是谁', 'knowledge_id': "3"}),
            Document(page_content='你会什么', metadata={
                'knowledge_title': '你会什么', 'knowledge_id': "4"}),
            Document(page_content='你能做什么', metadata={
                'knowledge_title': '你能做什么', 'knowledge_id': "5"}),
            Document(page_content='你能帮我做什么', metadata={
                'knowledge_title': '你能帮我做什么', 'knowledge_id': "6"}),
            Document(page_content='你能给我讲个笑话吗', metadata={
                'knowledge_title': '你能给我讲个笑话吗', 'knowledge_id': "7"}),
            Document(page_content='你能给我讲个故事吗', metadata={
                'knowledge_title': '你能给我讲个故事吗', 'knowledge_id': "8"}),
        ],
        embed_model_base_url='local:huggingface_embedding:BAAI/bge-small-zh-v1.5',
        embed_model_api_key=os.getenv('TEST_INFERENCE_TOKEN'),
        embed_model_name=os.getenv('TEST_BCE_EMBED_MODEL')
    )
    return request


def test_native_rag_ingest():
    rag = ElasticSearchRag()
    index_name = str(uuid.uuid4())
    rag.ingest(get_sample_request(index_name))

    metadata_update_request = DocumentMetadataUpdateRequest(
        index_name=index_name,
        metadata_filter={
            'knowledge_id': "8"
        },
        metadata={
            'knowledge_id': "8",
            'demo': '1111'
        }
    )
    rag.update_metadata(metadata_update_request)

    delete_req = DocumentDeleteRequest(
        index_name=index_name,
        metadata_filter={
            'knowledge_id': "8"
        }
    )
    rag.delete_document(delete_req)

    delete_index_req = IndexDeleteRequest(
        index_name=index_name
    )
    rag.delete_index(delete_index_req)


def test_native_rag():
    rag = ElasticSearchRag()
    index_name = str(uuid.uuid4())
    rag.ingest(get_sample_request(index_name))

    request = DocumentRetrieverRequest(
        index_name=index_name,
        search_query="你好",
        size=20,
        embed_model_base_url='local:huggingface_embedding:BAAI/bge-small-zh-v1.5',
        embed_model_api_key="",
        embed_model_name="bge-small-zh-v1.5",
        enable_rerank=True,
        rerank_model_base_url='local:bce:maidalun1020/bce-reranker-base_v1',
        rerank_top_k=5,
        rerank_model_api_key="",
        rerank_model_name="bce-reranker-base_v1",
    )

    result = rag.search(request)
    logger.info(result)

    delete_index_req = IndexDeleteRequest(
        index_name=index_name
    )
    rag.delete_index(delete_index_req)


def test_native_rag_with_local_models():
    rag = ElasticSearchRag()
    index_name = str(uuid.uuid4())
    rag.ingest(get_sample_request(index_name))

    request = DocumentRetrieverRequest(
        index_name=index_name,
        search_query="吗",
        size=20,
        embed_model_base_url="local:huggingface_embedding:BAAI/bge-small-zh-v1.5",
        embed_model_api_key="",
        embed_model_name="bge-small-zh-v1.5",
        enable_rerank=True,
        rerank_model_base_url=f'local:bce:maidalun1020/bce-reranker-base_v1',
        rerank_top_k=3,
        rerank_model_api_key="",
        rerank_model_name="bce-reranker-base_v1",
    )

    result = rag.search(request)
    logger.info(result)

    delete_index_req = IndexDeleteRequest(
        index_name=index_name
    )
    rag.delete_index(delete_index_req)


def test_native_rag_with_segment_recall():
    rag = ElasticSearchRag()
    index_name = str(uuid.uuid4())
    rag.ingest(get_sample_request(index_name))
    request = DocumentRetrieverRequest(
        index_name=index_name,
        search_query="rework",
        size=20,
        embed_model_base_url="local:huggingface_embedding:BAAI/bge-small-zh-v1.5",
        embed_model_api_key="",
        embed_model_name="bge-small-zh-v1.5",
        enable_rerank=False,
        rag_recall_mode='segment'
    )

    result = rag.search(request)
    logger.info(result)

    delete_index_req = IndexDeleteRequest(
        index_name=index_name
    )
    rag.delete_index(delete_index_req)


def test_native_rag_with_origin_recall():
    rag = ElasticSearchRag()
    index_name = str(uuid.uuid4())
    rag.ingest(get_sample_request(index_name))
    request = DocumentRetrieverRequest(
        index_name=index_name,
        search_query="rework",
        size=20,
        embed_model_base_url="local:huggingface_embedding:BAAI/bge-small-zh-v1.5",
        embed_model_api_key="",
        embed_model_name="bge-small-zh-v1.5",
        enable_rerank=False,
        rag_recall_mode='origin'
    )

    result = rag.search(request)
    logger.info(f"召回数量: {len(result)}")

    delete_index_req = IndexDeleteRequest(
        index_name=index_name
    )
    rag.delete_index(delete_index_req)
