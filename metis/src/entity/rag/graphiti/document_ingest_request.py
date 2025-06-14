from src.entity.rag.base.document_ingest_request import DocumentIngestRequest


class GraphitiRagDocumentIngestRequest(DocumentIngestRequest):
    openai_api_key: str = ''
    openai_model: str = ''
    openai_api_base: str = ''
    openai_small_model: str = ''

    rerank_model_base_url: str = ''
    rerank_model_name: str = ''
    rerank_model_api_key: str = ''

    group_id: str = ''

    rebuild_community: bool = False
