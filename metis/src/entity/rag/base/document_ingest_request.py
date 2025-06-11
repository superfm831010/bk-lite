from typing import List

from langchain_core.documents import Document
import openai
from pydantic import BaseModel


class DocumentIngestRequest(BaseModel):
    embed_model_base_url: str = ''
    embed_model_api_key: str = ''
    embed_model_name: str = ''

    index_name: str
    index_mode: str = ''
    chunk_size: int = 50
    max_chunk_bytes: int = 200000000
    docs: List[Document]


class GraphRagDocumentIngestRequest(DocumentIngestRequest):
    openai_api_key: str = ''
    openai_model: str = ''
    openai_api_base: str = ''
    openai_small_model: str = ''

    rerank_model_base_url: str = ''
    rerank_model_name: str = ''
    rerank_model_api_key: str = ''
