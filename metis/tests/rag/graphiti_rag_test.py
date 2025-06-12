
import os
import pytest
from src.chunk.fixed_size_chunk import FixedSizeChunk
from src.entity.rag.base.document_ingest_request import GraphRagDocumentIngestRequest
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

    chunk = FixedSizeChunk()
    loader = TextLoader(path='./tests/assert/full_text_loader.txt')
    docs = loader.load()
    rs = chunk.chunk(docs)

    request = GraphRagDocumentIngestRequest(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        openai_api_base=os.getenv('OPENAI_BASE_URL'),
        openai_model='gpt-4o',
        openai_small_model='gpt-4o',
        docs=rs,
        index_name="test_index",
        index_mode='overwrite',
        embed_model_base_url='local:huggingface_embedding:BAAI/bge-small-zh-v1.5',
        embed_model_api_key=os.getenv('TEST_INFERENCE_TOKEN'),
        embed_model_name=os.getenv('TEST_BCE_EMBED_MODEL'),
        rerank_model_api_key='',
        rerank_model_base_url='local:bce:maidalun1020/bce-reranker-base_v1',
        rerank_model_name='bce-reranker-base_v1',
    )
    await rag.ingest(request)
