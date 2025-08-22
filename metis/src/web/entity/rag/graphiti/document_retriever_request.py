from typing import List, Optional
from pydantic import BaseModel


class DocumentRetrieverRequest(BaseModel):
    embed_model_base_url: str = ''
    embed_model_api_key: Optional[str] = ''
    embed_model_name: Optional[str] = ''

    rerank_model_base_url: Optional[str] = ''
    rerank_model_api_key: Optional[str] = ''
    rerank_model_name: Optional[str] = ''

    size: Optional[int] = 100
    group_ids: Optional[List[str]] = []

    search_query: str = ''
