from pydantic import BaseModel


class DocumentDeleteRequest(BaseModel):
    uuid: str
