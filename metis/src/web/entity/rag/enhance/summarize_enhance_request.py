from typing import Optional

from pydantic import BaseModel


class SummarizeEnhanceRequest(BaseModel):
    content: str
    model: str = 'local:textrank'
    algorithm_args: Optional[dict] = {}


