from typing import List

from langchain_core.documents import Document
from sanic.log import logger

from src.web.entity.rag.base.document_retriever_request import DocumentRetrieverRequest
from src.core.rag.naive_rag.elasticsearch.elasticsearch_query_builder import ElasticsearchQueryBuilder
from src.core.rag.naive_rag.recall_strategies.base_recall_strategy import BaseRecallStrategy


class OriginRecallStrategy(BaseRecallStrategy):
    """Origin 召回策略 - 根据 knowledge_id 恢复原始文档片段"""
    
    def get_strategy_name(self) -> str:
        """获取策略名称"""
        return "origin"
    
    def process_recall(self, req: DocumentRetrieverRequest, search_result: List[Document], es_client) -> List[Document]:
        """
        处理 Origin 召回模式
        
        Args:
            req: 检索请求对象
            search_result: 初始搜索结果
            es_client: Elasticsearch 客户端
            
        Returns:
            处理后的搜索结果
        """
        # 1. 从搜索结果中提取所有相关的 knowledge_id
        knowledge_id_set = set()
        for doc in search_result:
            knowledge_id = doc.metadata['_source']['metadata'].get('knowledge_id')
            if knowledge_id:
                knowledge_id_set.add(knowledge_id)

        if not knowledge_id_set:
            logger.warning("没有找到有效的 knowledge_id，返回原始搜索结果")
            return search_result

        # 2. 查询 Elasticsearch 获取所有包含这些 knowledge_id 的文档
        knowledge_ids_filter = {
            "knowledge_id__in": list(knowledge_id_set)  # 使用 __in 语法
        }
        metadata_filter = ElasticsearchQueryBuilder.build_metadata_filter(knowledge_ids_filter)

        query = {
            "query": {"bool": {"filter": metadata_filter}},
            "from": 0,
            "size": 10000,
            "_source": {"excludes": ["vector"]}
        }

        response = es_client.search(index=req.index_name, body=query)

        # 3. 按 knowledge_id 组织文档
        knowledge_docs = {}
        for hit in response['hits']['hits']:
            source = hit['_source']
            metadata = source.get('metadata', {})
            knowledge_id = metadata.get('knowledge_id')

            if not knowledge_id:
                continue

            if knowledge_id not in knowledge_docs:
                knowledge_docs[knowledge_id] = []
            knowledge_docs[knowledge_id].append(hit)

        # 4. 返回所有匹配的文档
        result_hits = []
        for knowledge_id, hits in knowledge_docs.items():
            # 按 segment_number 排序
            sorted_hits = sorted(hits, key=lambda x: int(
                x['_source'].get('metadata', {}).get('segment_number', 0)))
            result_hits.extend(sorted_hits)

        logger.info(f"Origin 模式重组完成，共恢复 {len(result_hits)} 份文档片段")
        return self._convert_hits_to_documents(result_hits)

    def _convert_hits_to_documents(self, hits: List[dict]) -> List[Document]:
        """将 Elasticsearch hits 转换为 Document 对象"""
        docs_result = []
        for hit in hits:
            source = hit['_source']
            doc = Document(page_content=source['text'], metadata=hit)
            docs_result.append(doc)
        return docs_result
