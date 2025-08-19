from dataclasses import dataclass
from typing import Optional


@dataclass
class ReRankConfig:
    """重排序配置"""
    model_base_url: str
    model_name: str
    api_key: str
    query: str
    top_k: int
    threshold: Optional[float] = None