from typing import List
from pydantic import BaseModel


class RebuildCommunityRequest(BaseModel):
    group_ids: List[str] = []
