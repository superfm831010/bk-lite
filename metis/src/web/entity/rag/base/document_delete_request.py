from pydantic import BaseModel


class DocumentDeleteRequest(BaseModel):
    chunk_ids: list[str]
    knowledge_ids: list[str]
    keep_qa: bool
