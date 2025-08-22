from src.core.llm.entity.basic_llm_request import BasicLLMRequest


class AgentService:
    @classmethod
    def set_naive_rag_search_query(cls, body: BasicLLMRequest):
        for i in body.naive_rag_request:
            i.search_query = body.user_message
