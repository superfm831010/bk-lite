from typing import List

from src.core.entity.basic_llm_request import BasicLLMReuqest


class AgentService:
    @classmethod
    def set_naive_rag_search_query(cls, body: BasicLLMReuqest):
        for i in body.naive_rag_request:
            i.search_query = body.user_message
