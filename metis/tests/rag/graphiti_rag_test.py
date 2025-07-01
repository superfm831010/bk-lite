
import os

from src.chunk.full_chunk import FullChunk
from tqdm import tqdm
import pytest
from src.chunk.fixed_size_chunk import FixedSizeChunk
from src.chunk.recursive_chunk import RecursiveChunk
from src.entity.rag.base.index_delete_request import IndexDeleteRequest
from src.entity.rag.graphiti.document_delete_request import DocumentDeleteRequest
from src.entity.rag.graphiti.document_list_request import DocumentListRequest
from src.entity.rag.graphiti.document_ingest_request import GraphitiRagDocumentIngestRequest
from src.entity.rag.graphiti.document_retriever_request import DocumentRetrieverRequest
from src.loader.text_loader import TextLoader
from src.rag.graph_rag.graphiti.graphiti_rag import GraphitiRAG
from langchain_core.documents import Document
import glob


@pytest.mark.asyncio
async def test_setup_graph():
    rag = GraphitiRAG()
    await rag.setup_graph()


@pytest.mark.asyncio
async def test_ingest():
    rag = GraphitiRAG()

    chunk = RecursiveChunk(chunk_size=1024, chunk_overlap=128)
    loader = TextLoader(path='./tests/assert/content.txt')
    docs = loader.load()
    rs = chunk.chunk(docs)

    for i, doc in enumerate(rs):
        doc.metadata['knowledge_id'] = f'knowledge_{i}'
        doc.metadata['knowledge_title'] = 'development'
        doc.metadata['chunk_id'] = f'chunk_{i}'

    request = GraphitiRagDocumentIngestRequest(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        openai_api_base=os.getenv('OPENAI_BASE_URL'),
        openai_model='gpt-4.1-mini',
        docs=rs,
        embed_model_base_url='local:huggingface_embedding:BAAI/bge-small-zh-v1.5',
        embed_model_api_key=os.getenv('TEST_INFERENCE_TOKEN'),
        embed_model_name=os.getenv('TEST_BCE_EMBED_MODEL'),
        rerank_model_api_key='',
        rerank_model_base_url='local:bce:maidalun1020/bce-reranker-base_v1',
        rerank_model_name='bce-reranker-base_v1',
        rebuild_community=True,
        group_id='test_group',
    )
    await rag.ingest(request)


@pytest.mark.asyncio
async def test_retriver():
    rag = GraphitiRAG()
    request = DocumentRetrieverRequest(
        embed_model_base_url='local:huggingface_embedding:BAAI/bge-small-zh-v1.5',
        embed_model_api_key=os.getenv('TEST_INFERENCE_TOKEN'),
        embed_model_name=os.getenv('TEST_BCE_EMBED_MODEL'),
        rerank_model_api_key='',
        rerank_model_base_url='local:bce:maidalun1020/bce-reranker-base_v1',
        rerank_model_name='bce-reranker-base_v1',
        group_ids=['test_group'],
        search_query='CMDB如何写入主机',
        size=5
    )
    result = await rag.search(request)
    print(result)


@pytest.mark.asyncio
async def test_list_index_document():
    rag = GraphitiRAG()
    request = DocumentListRequest(
        group_ids=['test_group']
    )
    result = await rag.list_index_document(request)
    print(result)


@pytest.mark.asyncio
async def test_delete_document():
    rag = GraphitiRAG()
    request = DocumentDeleteRequest(
        uuid='58ea056e-30fa-40ad-8423-2d68d8e041fb'
    )
    await rag.delete_document(request)


@pytest.mark.asyncio
async def test_delete_index():
    rag = GraphitiRAG()
    request = IndexDeleteRequest(
        group_id='test_group'
    )
    await rag.delete_index(request)
