from typing import List

from langchain_core.documents import Document

from src.web.entity.rag.base.document_retriever_request import DocumentRetrieverRequest
from src.core.rag.naive_rag.elasticsearch.elasticsearch_query_builder import ElasticsearchQueryBuilder
from src.core.rag.naive_rag.recall_strategies.base_recall_strategy import BaseRecallStrategy


class SegmentRecallStrategy(BaseRecallStrategy):
    """Segment 召回策略 - 根据 segment_id 恢复段落片段"""
    
    def get_strategy_name(self) -> str:
        """获取策略名称"""
        return "segment"
    
    def process_recall(self, req: DocumentRetrieverRequest, search_result: List[Document], es_client) -> List[Document]:
        """
        处理 Segment 召回模式
        
        Args:
            req: 检索请求对象
            search_result: 初始搜索结果
            es_client: Elasticsearch 客户端
            
        Returns:
            处理后的搜索结果
        """
        # 1. 根据 chunk 的 segment_id 进行去重
        segments_id_set = set()
        for doc in search_result:
            segment_id = doc.metadata['_source']['metadata']['segment_id']
            segments_id_set.add(segment_id)

        # 2. 去 ElasticSearch 中查找所有的 segment_id 内容
        segment_ids_filter = {
            "segment_id__in": list(segments_id_set)  # 使用 __in 语法
        }
        metadata_filter = ElasticsearchQueryBuilder.build_metadata_filter(segment_ids_filter)

        query = {
            "query": {"bool": {"filter": metadata_filter}},
            "from": 0,
            "size": 10000,
            "_source": {"excludes": ["vector"]}
        }
        
        response = es_client.search(index=req.index_name, body=query)
        
        # 3. 按 segment_id 分组处理
        segment_id_dict = {}
        for hit in response['hits']['hits']:
            source = hit['_source']
            metadata = source.get('metadata', {})
            segment_id = metadata.get('segment_id')
            if segment_id not in segment_id_dict:
                segment_id_dict[segment_id] = []
            segment_id_dict[segment_id].append(hit)

        # 4. 按 segment_id 分组处理并排序
        result_hits = []
        for segment_id, hits in segment_id_dict.items():
            # 按 chunk_number 排序
            sorted_hits = sorted(hits, key=lambda x: int(
                x['_source'].get('metadata', {}).get('chunk_number', 0)))
            result_hits.extend(sorted_hits)

        return self._convert_hits_to_documents(result_hits)

    def _convert_hits_to_documents(self, hits: List[dict]) -> List[Document]:
        """将 Elasticsearch hits 转换为 Document 对象"""
        docs_result = []
        for hit in hits:
            source = hit['_source']
            doc = Document(page_content=source['text'], metadata=hit)
            docs_result.append(doc)
        return docs_result
