import copy
import os
from typing import List

import elasticsearch
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchRetriever
from langchain_elasticsearch import ElasticsearchStore
from sanic.log import logger

from src.core.env.core_settings import core_settings
from src.embed.embed_builder import EmbedBuilder
from src.entity.rag.base.document_count_request import DocumentCountRequest
from src.entity.rag.base.document_delete_request import DocumentDeleteRequest
from src.entity.rag.base.document_ingest_request import DocumentIngestRequest
from src.entity.rag.base.document_list_request import DocumentListRequest
from src.entity.rag.base.document_metadata_update_request import DocumentMetadataUpdateRequest
from src.entity.rag.base.document_retriever_request import DocumentRetrieverRequest
from src.entity.rag.base.index_delete_request import IndexDeleteRequest
from src.rag.base_rag import BaseRag
from src.rag.naive_rag.elasticsearch.elasticsearch_query_builder import ElasticsearchQueryBuilder
from src.rerank.rerank_manager import ReRankManager


class ElasticSearchRag(BaseRag):
    """Elasticsearch RAG 实现类"""
    
    def __init__(self):
        self.es = elasticsearch.Elasticsearch(
            hosts=[core_settings.elasticsearch_url],
            basic_auth=("elastic", core_settings.elasticsearch_password)
        )

    def update_metadata(self, req: DocumentMetadataUpdateRequest):
        """
        根据过滤条件更新文档的元数据

        Args:
            req: 包含索引名称、元数据过滤条件和新元数据的请求对象

        Returns:
            更新的文档数量
        """
        # 构建过滤条件
        metadata_filter = []
        for key, value in req.metadata_filter.items():
            # 检查值是否为逗号分隔的字符串
            if isinstance(value, str) and ',' in value:
                # 按逗号分割并去除空白
                values = [v.strip() for v in value.split(',')]
                metadata_filter.append(
                    {"terms": {f"metadata.{key}.keyword": values}}
                )
            else:
                metadata_filter.append(
                    {"term": {f"metadata.{key}.keyword": value}}
                )

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

    def count_index_document(self, req: DocumentCountRequest):
        if not req.metadata_filter:
            # Count all documents in the index
            count = self.es.count(index=req.index_name)
            return count['count']

        # Build filter query for specific metadata
        metadata_filter = []
        for key, value in req.metadata_filter.items():
            metadata_filter.append(
                {"term": {f"metadata.{key}.keyword": value}})

        # Build the query with metadata filter
        query = {
            "query": {
                "bool": {
                    "filter": metadata_filter
                }
            }
        }

        # Add match_phrase query if req.query is not empty
        if req.query:
            if not query["query"]["bool"].get("must"):
                query["query"]["bool"]["must"] = []
                query["query"]["bool"]["must"].append({
                    "match_phrase": {
                        "text": req.query
                    }
                })

        count = self.es.count(index=req.index_name, body=query)
        return count['count']

    def delete_index(self, req: IndexDeleteRequest):
        self.es.indices.delete(index=req.index_name)

    def list_index_document(self, req: DocumentListRequest):
        # Build filter query for specific metadata
        metadata_filter = ElasticsearchQueryBuilder.build_metadata_filter(
            req.metadata_filter)

        # Calculate offset from page and size
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

        # Add match_phrase query if req.query is not empty
        if req.query:
            if not query["query"]["bool"].get("must"):
                query["query"]["bool"]["must"] = []
                query["query"]["bool"]["must"].append({
                    "match_phrase": {
                        "text": req.query
                    }
                })

        # Execute the search query
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
        metadata_filter = []
        for key, value in req.metadata_filter.items():
            # Check if the value is a comma-separated string
            if isinstance(value, str) and ',' in value:
                # Split the value by comma and strip whitespace
                values = [v.strip() for v in value.split(',')]
                metadata_filter.append(
                    {"terms": {f"metadata.{key}.keyword": values}}
                )
            else:
                metadata_filter.append(
                    {"term": {f"metadata.{key}.keyword": value}}
                )

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
        
        if recall_mode == 'chunk':
            return search_result
        elif recall_mode == 'segment':
            return self._process_segment_recall(req, search_result)
        elif recall_mode == 'origin':
            return self._process_origin_recall(req, search_result)
        else:
            logger.warning(f"不支持的召回模式: {recall_mode}")
            return search_result

    def _process_segment_recall(self, req: DocumentRetrieverRequest, search_result: List[Document]) -> List[Document]:
        """处理Segment召回模式"""
        # 1. 根据chunk的segment_id进行去重
        segments_id_set = set()
        for doc in search_result:
            segment_id = doc.metadata['_source']['metadata']['segment_id']
            segments_id_set.add(segment_id)

        # 2. 去ElasticSearch中查找所有的segment_id内容
        segment_id_dict = {}
        metadata_filter = [
            {
                "terms": {
                    "metadata.segment_id.keyword": list(segments_id_set)
                }
            }
        ]

        query = {
            "query": {"bool": {"filter": metadata_filter}},
            "from": 0,
            "size": 10000,
            "_source": {"excludes": ["vector"]}
        }
        
        response = self.es.search(index=req.index_name, body=query)
        for hit in response['hits']['hits']:
            source = hit['_source']
            metadata = source.get('metadata', {})
            segment_id = metadata.get('segment_id')
            if segment_id not in segment_id_dict:
                segment_id_dict[segment_id] = []
            segment_id_dict[segment_id].append(hit)

        # 3. 按segment_id分组处理
        search_result = []
        for segment_id, hits in segment_id_dict.items():
            # 按chunk_number排序
            sorted_hits = sorted(hits, key=lambda x: int(
                x['_source'].get('metadata', {}).get('chunk_number', 0)))
            search_result.extend(sorted_hits)

        return self._convert_hits_to_documents(search_result)

    def _process_origin_recall(self, req: DocumentRetrieverRequest, search_result: List[Document]) -> List[Document]:
        """处理Origin召回模式"""
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
        metadata_filter = [
            {
                "terms": {
                    "metadata.knowledge_id.keyword": list(knowledge_id_set)
                }
            }
        ]

        query = {
            "query": {"bool": {"filter": metadata_filter}},
            "from": 0,
            "size": 10000,
            "_source": {"excludes": ["vector"]}
        }

        response = self.es.search(index=req.index_name, body=query)

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
        search_result = []
        for knowledge_id, hits in knowledge_docs.items():
            # 按segment_number排序
            sorted_hits = sorted(hits, key=lambda x: int(
                x['_source'].get('metadata', {}).get('segment_number', 0)))
            search_result.extend(sorted_hits)

        logger.info(f"Origin 模式重组完成，共恢复 {len(search_result)} 份文档片段")
        return self._convert_hits_to_documents(search_result)

    def _convert_hits_to_documents(self, hits: List[dict]) -> List[Document]:
        """将 Elasticsearch hits 转换为 Document 对象"""
        docs_result = []
        for hit in hits:
            source = hit['_source']
            doc = Document(page_content=source['text'], metadata=hit)
            docs_result.append(doc)
        return docs_result
