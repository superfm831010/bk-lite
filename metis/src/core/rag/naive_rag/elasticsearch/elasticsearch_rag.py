import copy
from typing import List

import elasticsearch
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchRetriever
from langchain_elasticsearch import ElasticsearchStore
from sanic.log import logger

from src.core.embed.embed_builder import EmbedBuilder
from src.core.rerank.rerank_manager import ReRankManager
from src.core.sanic_plus.env.core_settings import core_settings
from src.web.entity.rag.base.document_count_request import DocumentCountRequest
from src.web.entity.rag.base.document_delete_request import DocumentDeleteRequest
from src.web.entity.rag.base.document_ingest_request import DocumentIngestRequest
from src.web.entity.rag.base.document_list_request import DocumentListRequest
from src.web.entity.rag.base.document_metadata_update_request import DocumentMetadataUpdateRequest
from src.web.entity.rag.base.document_retriever_request import DocumentRetrieverRequest
from src.web.entity.rag.base.index_delete_request import IndexDeleteRequest
from src.core.rag.base_rag import BaseRag
from src.core.rag.naive_rag.elasticsearch.elasticsearch_query_builder import ElasticsearchQueryBuilder
from src.core.rag.naive_rag.recall_strategies.recall_strategy_factory import RecallStrategyFactory


class ElasticSearchRag(BaseRag):
    """Elasticsearch RAG 实现类"""

    def __init__(self):
        self.es = elasticsearch.Elasticsearch(
            hosts=[core_settings.elasticsearch_url],
            basic_auth=("elastic", core_settings.elasticsearch_password)
        )

    def update_metadata(self, req: DocumentMetadataUpdateRequest):
        metadata_filter = ElasticsearchQueryBuilder.build_metadata_filter(
            req.metadata_filter)

        # 构建查询
        query = {
            "query": {
                "bool": {
                    "filter": metadata_filter
                }
            }
        }

        # 构建更新脚本
        script_parts = []
        for key, value in req.metadata.items():
            script_parts.append(f'ctx._source.metadata.{key} = params.{key}')

        update_script = {
            "script": {
                "source": "; ".join(script_parts),
                "params": req.metadata
            }
        }

        # 执行更新
        self.es.update_by_query(
            index=req.index_name,
            body={**query, **update_script}
        )
        self.es.indices.refresh(index=req.index_name)

    def count_index_document(self, req: DocumentCountRequest) -> int:
        """
        统计索引中符合条件的文档数量

        Args:
            req: 文档计数请求对象

        Returns:
            符合条件的文档数量
        """
        # 如果没有任何过滤条件，直接返回索引总数
        if not req.metadata_filter and not req.query:
            logger.debug(f"Counting all documents in index: {req.index_name}")
            count = self.es.count(index=req.index_name)
            return count['count']

        # 构建查询条件
        query_body = {"query": {"bool": {}}}

        # 添加元数据过滤条件
        if req.metadata_filter:
            metadata_filter = ElasticsearchQueryBuilder.build_metadata_filter(
                req.metadata_filter)
            query_body["query"]["bool"]["filter"] = metadata_filter

        # 添加文本匹配条件
        if req.query:
            query_body["query"]["bool"]["must"] = [{
                "match_phrase": {"text": req.query}
            }]

        count = self.es.count(index=req.index_name, body=query_body)
        return count['count']

    def delete_index(self, req: IndexDeleteRequest):
        self.es.indices.delete(index=req.index_name)

    def list_index_document(self, req: DocumentListRequest):
        metadata_filter = ElasticsearchQueryBuilder.build_metadata_filter(
            req.metadata_filter)

        offset = (req.page - 1) * req.size if req.page > 0 else 0

        # Build the query
        query = {
            "query": {
                "bool": {
                    "filter": metadata_filter
                }
            },
            "from": offset,
            "size": req.size,
            "_source": {"excludes": ["vector"]}  # Exclude the vector field
        }

        # Add sorting with backward compatibility and field existence check
        if req.sort_field and req.sort_order:
            # 验证排序方式
            sort_order = req.sort_order.lower()
            if sort_order not in ['asc', 'desc']:
                sort_order = 'desc'  # 默认降序

            # 检查字段是否存在于索引映射中
            field_exists = self._check_field_exists_in_mapping(
                req.index_name, req.sort_field)

            if field_exists:
                # 字段存在，可以安全排序
                sort_config = {req.sort_field: {"order": sort_order}}

                # 如果是时间字段排序，添加缺失值处理
                if 'created_time' in req.sort_field or 'updated_time' in req.sort_field:
                    sort_config[req.sort_field]["missing"] = "_last" if sort_order == 'asc' else "_first"
                    logger.debug(
                        f"时间字段排序，添加兼容性处理: 缺失值放在{'最后' if sort_order == 'asc' else '最前'}")

                query["sort"] = [sort_config]
            else:
                # 可以选择使用一个默认的排序字段，比如 _score
                query["sort"] = [{"_score": {"order": "desc"}}]

        # Add match_phrase query if req.query is not empty
        if req.query:
            query["query"]["bool"]["must"] = []
            query["query"]["bool"]["must"].append({
                "match_phrase": {
                    "text": req.query
                }
            })

        response = self.es.search(index=req.index_name, body=query)

        # Process and return the results
        documents = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            metadata = source.get('metadata', {})
            documents.append(
                Document(page_content=source['text'], metadata=metadata))

        return documents

    def delete_document(self, req: DocumentDeleteRequest):
        metadata_filter = ElasticsearchQueryBuilder.build_metadata_filter(
            req.metadata_filter)

        query = {
            "query": {
                "bool": {
                    "filter": metadata_filter
                }
            }
        }

        self.es.delete_by_query(index=req.index_name, body=query)

    def ingest(self, req: DocumentIngestRequest):

        if req.index_mode == 'overwrite' and self.es.indices.exists(index=req.index_name):
            self.es.indices.delete(index=req.index_name)

        embedding = EmbedBuilder.get_embed(req.embed_model_base_url,
                                           req.embed_model_name,
                                           req.embed_model_api_key,
                                           req.embed_model_base_url)
        db = ElasticsearchStore.from_documents(
            req.docs, embedding=embedding,
            es_connection=self.es, index_name=req.index_name,
            bulk_kwargs={
                "chunk_size": req.chunk_size,
                "max_chunk_bytes": req.max_chunk_bytes
            }
        )
        db.client.indices.refresh(index=req.index_name)

    def _process_search_result(self, docs: List[Document]) -> List[Document]:
        """处理搜索结果，移除向量字段并添加QA答案"""
        for doc in docs:
            if 'vector' in doc.metadata.get('_source', {}):
                del doc.metadata['_source']['vector']
            if 'qa_answer' in doc.metadata.get('_source', {}).get('metadata', {}):
                doc.page_content += f"\n{doc.metadata['_source']['metadata']['qa_answer']}"
        return docs

    def _rerank_results(self, req: DocumentRetrieverRequest, search_result: List[Document]) -> List[Document]:
        """重排序处理"""
        if not search_result:
            return search_result

        # 准备重排序参数
        rerank_kwargs = {
            'rerank_model_base_url': req.rerank_model_base_url,
            'rerank_model_name': req.rerank_model_name,
            'rerank_model_api_key': req.rerank_model_api_key,
            'search_query': req.search_query,
            'search_result': search_result,
            'rerank_top_k': req.rerank_top_k,
        }

        # 只有当阈值存在且大于0时才传递阈值参数
        if hasattr(req, 'threshold') and req.threshold is not None and req.threshold > 0:
            rerank_kwargs['threshold'] = req.threshold

        return ReRankManager.rerank_documents(**rerank_kwargs)

    def _create_retriever(self, req: DocumentRetrieverRequest) -> ElasticsearchRetriever:
        """创建Elasticsearch检索器"""
        return ElasticsearchRetriever.from_es_params(
            index_name=req.index_name,
            body_func=lambda x: ElasticsearchQueryBuilder.build_query(req),
            content_field="text",
            url=core_settings.elasticsearch_url,
            username="elastic",
            password=core_settings.elasticsearch_password,
        )

    def _execute_rag_search(self, req: DocumentRetrieverRequest, rag_type: str) -> List[Document]:
        """执行RAG搜索的通用方法"""
        rag_request = copy.deepcopy(req)

        # 根据RAG类型设置不同的过滤条件
        if rag_type == 'naive':
            rag_request.metadata_filter['qa_answer__missing'] = True
        elif rag_type == 'qa':
            rag_request.metadata_filter['qa_answer__exists'] = True

        # 执行搜索
        documents_retriever = self._create_retriever(rag_request)
        search_results = documents_retriever.invoke(req.search_query)
        search_results = self._process_search_result(search_results)

        # 重排序处理
        if req.enable_rerank:
            search_results = self._rerank_results(req, search_results)
            # 只有naive RAG需要召回阶段处理
            if rag_type == 'naive':
                search_results = self.process_recall_stage(req, search_results)

        return search_results

    def search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """
        搜索符合条件的文档

        Args:
            req: 检索请求对象

        Returns:
            检索到的文档列表
        """
        search_result = []

        if req.enable_naive_rag:
            naive_results = self._execute_rag_search(req, 'naive')
            search_result.extend(naive_results)

        if req.enable_qa_rag:
            qa_results = self._execute_rag_search(req, 'qa')
            search_result.extend(qa_results)

        return search_result

    def process_recall_stage(self, req: DocumentRetrieverRequest, search_result: List[Document]) -> List[Document]:
        """
        处理检索阶段，根据不同的召回模式处理搜索结果

        Args:
            req: 检索请求对象
            search_result: 初始搜索结果

        Returns:
            处理后的搜索结果
        """
        recall_mode = getattr(req, 'rag_recall_mode', 'chunk')

        try:
            strategy = RecallStrategyFactory.get_strategy(recall_mode)
            return strategy.process_recall(req, search_result, self.es)
        except ValueError as e:
            logger.warning(str(e))
            # 如果策略不存在，回退到默认的chunk模式
            default_strategy = RecallStrategyFactory.get_strategy('chunk')
            return default_strategy.process_recall(req, search_result, self.es)

    def _convert_hits_to_documents(self, hits: List[dict]) -> List[Document]:
        """将 Elasticsearch hits 转换为 Document 对象"""
        docs_result = []
        for hit in hits:
            source = hit['_source']
            doc = Document(page_content=source['text'], metadata=hit)
            docs_result.append(doc)
        return docs_result

    def _check_field_exists_in_mapping(self, index_name: str, field_path: str) -> bool:
        """
        检查字段是否存在于索引映射中

        Args:
            index_name: 索引名称
            field_path: 字段路径，例如 'metadata.created_time'

        Returns:
            bool: 字段是否存在
        """
        try:
            # 获取索引映射
            mapping_response = self.es.indices.get_mapping(index=index_name)

            if index_name not in mapping_response:
                logger.warning(f"索引 {index_name} 不存在")
                return False

            mappings = mapping_response[index_name]['mappings']

            # 检查字段路径是否存在
            field_parts = field_path.split('.')
            current_mapping = mappings.get('properties', {})

            for part in field_parts:
                if part in current_mapping:
                    if 'properties' in current_mapping[part]:
                        # 这是一个对象字段，继续向下查找
                        current_mapping = current_mapping[part]['properties']
                    else:
                        # 这是最终字段
                        if part == field_parts[-1]:
                            logger.debug(
                                f"字段 {field_path} 在索引 {index_name} 中存在")
                            return True
                        else:
                            # 路径中断，字段不存在
                            logger.debug(
                                f"字段路径 {field_path} 在索引 {index_name} 中不完整")
                            return False
                else:
                    logger.debug(f"字段 {field_path} 在索引 {index_name} 中不存在")
                    return False

            return True

        except Exception as e:
            logger.error(f"检查字段映射时出错: {str(e)}")
            return False
