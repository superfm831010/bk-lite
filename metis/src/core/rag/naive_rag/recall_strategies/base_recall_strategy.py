from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document

from src.web.entity.rag.base.document_retriever_request import DocumentRetrieverRequest


class BaseRecallStrategy(ABC):
    """召回策略基类"""
    
    @abstractmethod
    def process_recall(self, req: DocumentRetrieverRequest, search_result: List[Document], es_client) -> List[Document]:
        """
        处理召回逻辑
        
        Args:
            req: 检索请求对象
            search_result: 初始搜索结果
            es_client: Elasticsearch 客户端
            
        Returns:
            处理后的搜索结果
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        获取策略名称
        
        Returns:
            策略名称
        """
        pass
