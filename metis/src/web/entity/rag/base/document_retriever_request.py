from typing import Optional

from pydantic import BaseModel

from src.web.entity.rag.graphiti.document_retriever_request import \
    DocumentRetrieverRequest as GraphitiDocumentRetrieverRequest


class DocumentRetrieverRequest(BaseModel):
    index_name: str
    search_query: str = ''
    metadata_filter: Optional[dict] = {}

    threshold: Optional[float] = 0.7
    enable_term_search: Optional[bool] = True

    text_search_weight: Optional[float] = 0.9
    text_search_mode: Optional[str] = 'match'

    enable_vector_search: Optional[bool] = True
    vector_search_weight: Optional[float] = 0.1

    rag_k: Optional[int] = 10
    rag_num_candidates: Optional[int] = 1000
    enable_rerank: Optional[bool] = False

    embed_model_base_url: Optional[str] = ''
    embed_model_api_key: Optional[str] = ''
    embed_model_name: str = ''

    rerank_model_base_url: Optional[str] = ''
    rerank_model_api_key: Optional[str] = ''
    rerank_model_name: Optional[str] = ''
    rerank_top_k: Optional[int] = 5

    rag_recall_mode: Optional[str] = "chunk"

    size: int = 100
    enable_naive_rag: Optional[bool] = True

    enable_qa_rag: Optional[bool] = False
    qa_size: int = 10

    enable_graph_rag: Optional[bool] = False
    graph_rag_request: Optional[GraphitiDocumentRetrieverRequest] = None
