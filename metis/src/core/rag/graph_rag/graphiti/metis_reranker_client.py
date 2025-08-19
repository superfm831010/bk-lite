from graphiti_core.cross_encoder.client import CrossEncoderClient
from langchain_core.documents import Document
from src.core.rag.graph_rag.graphiti.metis_raranker_config import MetisRerankerConfig
from sanic.log import logger

from src.core.rerank.entity.rerank_config import ReRankConfig
from src.core.rerank.rerank_manager import ReRankManager


class MetisRerankerClient(CrossEncoderClient):
    def __init__(self, config: MetisRerankerConfig):
        self.config = config

    async def rank(self, query: str, passages: list[str]) -> list[tuple[str, float]]:
        """重排序方法，返回(文档内容, 分数)的元组列表"""
        try:
            # 将passages转换为Document对象
            documents = [Document(page_content=passage) for passage in passages]
            
            # 创建重排序配置
            rerank_config = ReRankConfig(
                model_base_url=self.config.url,
                model_name=self.config.model_name,
                api_key=self.config.api_key,
                query=query,
                top_k=len(passages)  # 返回所有文档
            )
            
            # 执行重排序
            reranked_docs = ReRankManager.rerank_documents_with_config(rerank_config, documents)
            
            # 转换为graphiti需要的格式：(内容, 分数)
            result = []
            for doc in reranked_docs:
                score = doc.metadata.get('relevance_score', 0.0) if hasattr(doc, 'metadata') else 0.0
                result.append((doc.page_content, score))
            
            return result
            
        except Exception as e:
            logger.error(f"重排序失败: {e}")
            # 如果重排序失败，返回原始顺序且分数为0
            return [(passage, 0.0) for passage in passages]
