from pydantic import BaseModel


class DocumentMetadataUpdateRequest(BaseModel):
    knowledge_ids: list[str] = []
    chunk_ids: list[str] = []
    metadata: dict = {}
