
import os
import pytest
from src.chunk.fixed_size_chunk import FixedSizeChunk
from src.chunk.recursive_chunk import RecursiveChunk
from src.entity.rag.graphiti.document_ingest_request import GraphitiRagDocumentIngestRequest
from src.loader.text_loader import TextLoader
from src.rag.graph_rag.graphiti.graphiti_rag import GraphitiRAG
from langchain_core.documents import Document


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

    request = GraphitiRagDocumentIngestRequest(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        openai_api_base=os.getenv('OPENAI_BASE_URL'),
        openai_model='gpt-4.1-mini',
        openai_small_model='gpt-4.1-nano',
        docs=rs,
        index_name="test_index",
        index_mode='overwrite',
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
