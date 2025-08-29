from typing import List

from langchain_core.documents import Document
from sanic.log import logger

from src.web.entity.rag.base.document_retriever_request import DocumentRetrieverRequest
from src.web.entity.rag.base.document_list_request import DocumentListRequest
from src.core.rag.naive_rag.recall_strategies.base_recall_strategy import BaseRecallStrategy


class OriginRecallStrategy(BaseRecallStrategy):
    """Origin 召回策略 - 根据 knowledge_id 恢复原始文档片段"""

    def get_strategy_name(self) -> str:
        """获取策略名称"""
        return "origin"

    def process_recall(self, req: DocumentRetrieverRequest, search_result: List[Document], rag_client) -> List[Document]:
        """
        处理 Origin 召回模式

        Args:
            req: 检索请求对象
            search_result: 初始搜索结果
            rag_client: RAG客户端 (PgvectorRag)

        Returns:
            处理后的搜索结果
        """
        # 1. 从搜索结果中提取所有相关的 knowledge_id
        knowledge_id_set = set()
        for doc in search_result:
            knowledge_id = doc.metadata.get('knowledge_id')
            if knowledge_id:
                knowledge_id_set.add(knowledge_id)

        if not knowledge_id_set:
            logger.warning("没有找到有效的 knowledge_id，返回原始搜索结果")
            return search_result

        # 2. 通过RAG客户端查找所有的 knowledge_id 内容
        try:
            # 使用PgvectorRag的list_index_document方法查询
            list_req = DocumentListRequest(
                index_name=req.index_name,
                metadata_filter={"knowledge_id__in": list(knowledge_id_set)},
                page=0,
                size=10000
            )
            all_knowledge_docs = rag_client.list_index_document(list_req)

            logger.info(f"Origin模式查询完成，找到 {len(all_knowledge_docs)} 个相关片段")

        except Exception as e:
            logger.error(f"Origin召回查询失败: {e}")
            return search_result

        # 3. 按 knowledge_id 组织文档
        knowledge_docs = {}
        for doc in all_knowledge_docs:
            knowledge_id = doc.metadata.get('knowledge_id')
            if knowledge_id:
                if knowledge_id not in knowledge_docs:
                    knowledge_docs[knowledge_id] = []
                knowledge_docs[knowledge_id].append(doc)

        # 4. 返回所有匹配的文档
        result_hits = []
        for knowledge_id, docs in knowledge_docs.items():
            # 按 segment_number 排序
            sorted_docs = sorted(docs, key=lambda x: int(
                x.metadata.get('segment_number', 0)))
            result_hits.extend(sorted_docs)

        logger.info(f"Origin 模式重组完成，共恢复 {len(result_hits)} 份文档片段")
        return result_hits
