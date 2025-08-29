from typing import List

from langchain_core.documents import Document
from sanic.log import logger

from src.web.entity.rag.base.document_retriever_request import DocumentRetrieverRequest
from src.web.entity.rag.base.document_list_request import DocumentListRequest
from src.core.rag.naive_rag.recall_strategies.base_recall_strategy import BaseRecallStrategy


class SegmentRecallStrategy(BaseRecallStrategy):
    """Segment 召回策略 - 根据 segment_id 恢复段落片段"""

    def get_strategy_name(self) -> str:
        """获取策略名称"""
        return "segment"

    def process_recall(self, req: DocumentRetrieverRequest, search_result: List[Document], rag_client) -> List[Document]:
        """
        处理 Segment 召回模式

        Args:
            req: 检索请求对象
            search_result: 初始搜索结果
            rag_client: RAG客户端 (PgvectorRag)

        Returns:
            处理后的搜索结果
        """
        # 1. 从搜索结果中提取所有相关的 segment_id
        segments_id_set = set()
        for doc in search_result:
            segment_id = doc.metadata.get('segment_id')
            if segment_id:
                segments_id_set.add(segment_id)

        if not segments_id_set:
            logger.warning("没有找到有效的 segment_id，返回原始搜索结果")
            return search_result

        # 2. 通过RAG客户端查找所有的 segment_id 内容
        try:
            # 使用PgvectorRag的list_index_document方法查询
            list_req = DocumentListRequest(
                index_name=req.index_name,
                metadata_filter={"segment_id__in": list(segments_id_set)},
                page=0,
                size=10000
            )
            all_segment_docs = rag_client.list_index_document(list_req)

            logger.info(f"Segment模式查询完成，找到 {len(all_segment_docs)} 个相关片段")

        except Exception as e:
            logger.error(f"Segment召回查询失败: {e}")
            return search_result

        # 3. 按 segment_id 分组处理
        segment_id_dict = {}
        for doc in all_segment_docs:
            segment_id = doc.metadata.get('segment_id')
            if segment_id:
                if segment_id not in segment_id_dict:
                    segment_id_dict[segment_id] = []
                segment_id_dict[segment_id].append(doc)

        # 4. 按 segment_id 分组处理并排序
        result_hits = []
        for segment_id, docs in segment_id_dict.items():
            # 按 chunk_number 排序
            sorted_docs = sorted(docs, key=lambda x: int(
                x.metadata.get('chunk_number', 0)))
            result_hits.extend(sorted_docs)

        logger.info(f"Segment模式重组完成，共恢复 {len(result_hits)} 份文档片段")
        return result_hits
