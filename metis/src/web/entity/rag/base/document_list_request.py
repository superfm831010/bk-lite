from typing import Optional
from pydantic import BaseModel, Field


class DocumentListRequest(BaseModel):
    index_name: str
    page: int
    size: int
    metadata_filter: dict
    query: str
    sort_field: Optional[str] = Field(
        default="created_time", description="排序字段，默认为创建时间")
    sort_order: Optional[str] = Field(
        default="desc", description="排序方式，支持asc/desc，默认为desc")
