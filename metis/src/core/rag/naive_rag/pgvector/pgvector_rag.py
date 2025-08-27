import copy
import json
from typing import List, Dict, Any, Optional

import psycopg
from langchain_core.documents import Document
from langchain_postgres import PGVector
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
from src.core.rag.naive_rag.recall_strategies.recall_strategy_factory import RecallStrategyFactory


class PgvectorRag(BaseRag):
    """基于PostgreSQL + pgvector的RAG实现"""

    def __init__(self):
        pass

    def _execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """执行SQL查询"""
        try:
            with psycopg.connect(core_settings.db_uri) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params or {})
                    if cur.description:
                        columns = [desc[0] for desc in cur.description]
                        return [dict(zip(columns, row)) for row in cur.fetchall()]
                    return []
        except Exception as e:
            logger.error(f"SQL执行失败: {e}")
            raise

    def _get_chunk_ids_by_knowledge_ids(self, knowledge_ids: List[str]) -> List[str]:
        """根据knowledge_ids查询chunk_ids"""
        if not knowledge_ids:
            return []

        query = """
            SELECT id FROM langchain_pg_embedding 
            WHERE cmetadata->>'knowledge_id' = ANY(%(knowledge_ids)s)
        """
        results = self._execute_query(query, {'knowledge_ids': knowledge_ids})
        return [result['id'] for result in results]

    def _collect_target_chunk_ids(self, chunk_ids: Optional[List[str]], knowledge_ids: Optional[List[str]]) -> List[str]:
        """收集要处理的chunk_ids"""
        all_chunk_ids = []

        if chunk_ids:
            all_chunk_ids.extend(chunk_ids)

        if knowledge_ids:
            found_chunk_ids = self._get_chunk_ids_by_knowledge_ids(
                knowledge_ids)
            all_chunk_ids.extend(found_chunk_ids)

        return list(set(all_chunk_ids))  # 去重

    def _build_metadata_filter(self, metadata_filter: dict, params: Dict[str, Any]) -> str:
        """构建元数据过滤条件"""
        if not metadata_filter:
            return ""

        conditions = []
        for key, value in metadata_filter.items():
            param_key = f"metadata_{key}".replace(".", "_")

            if key.endswith("__exists"):
                field_key = key.replace("__exists", "")
                conditions.append(
                    f"e.cmetadata ? %(metadata_{field_key}_exists)s")
                params[f"metadata_{field_key}_exists"] = field_key
            elif key.endswith("__missing"):
                field_key = key.replace("__missing", "")
                conditions.append(
                    f"NOT (e.cmetadata ? %(metadata_{field_key}_missing)s)")
                params[f"metadata_{field_key}_missing"] = field_key
            elif key.endswith("__like"):
                field_key = key.replace("__like", "")
                conditions.append(
                    f"e.cmetadata->>%({param_key}_field)s LIKE %({param_key}_value)s")
                params[f"{param_key}_field"] = field_key
                params[f"{param_key}_value"] = str(value)
            elif key.endswith("__ilike"):
                field_key = key.replace("__ilike", "")
                conditions.append(
                    f"e.cmetadata->>%({param_key}_field)s ILIKE %({param_key}_value)s")
                params[f"{param_key}_field"] = field_key
                params[f"{param_key}_value"] = str(value)
            else:
                conditions.append(
                    f"e.cmetadata->>%({param_key}_field)s = %({param_key}_value)s")
                params[f"{param_key}_field"] = key
                params[f"{param_key}_value"] = str(value)

        return "(" + " AND ".join(conditions) + ")" if conditions else ""

    def _build_where_clauses(self, req, where_clauses: List[str], params: Dict[str, Any]) -> None:
        """构建WHERE子句"""
        where_clauses.append("c.name = %(index_name)s")
        params['index_name'] = req.index_name

        if hasattr(req, 'metadata_filter') and req.metadata_filter:
            metadata_condition = self._build_metadata_filter(
                req.metadata_filter, params)
            if metadata_condition:
                where_clauses.append(metadata_condition)

        if hasattr(req, 'query') and req.query:
            where_clauses.append("e.document ILIKE %(query_pattern)s")
            params['query_pattern'] = f"%{req.query}%"

    def update_metadata(self, req: DocumentMetadataUpdateRequest) -> None:
        """更新文档元数据"""
        chunk_ids = self._collect_target_chunk_ids(
            req.chunk_ids, req.knowledge_ids)

        if not chunk_ids:
            logger.warning("未找到要更新的文档")
            return

        logger.info(f"开始更新元数据，chunk数量: {len(chunk_ids)}")

        query = """
            UPDATE langchain_pg_embedding 
            SET cmetadata = cmetadata || %(new_metadata)s::jsonb
            WHERE id = ANY(%(chunk_ids)s)
        """
        params = {
            'new_metadata': json.dumps(req.metadata),
            'chunk_ids': chunk_ids
        }

        try:
            self._execute_query(query, params)
            logger.info(f"元数据更新成功，影响记录: {len(chunk_ids)}个")
        except Exception as e:
            logger.error(f"元数据更新失败: {e}")
            raise

    def count_index_document(self, req: DocumentCountRequest) -> int:
        """统计索引中符合条件的文档数量"""
        where_clauses = []
        params = {}
        self._build_where_clauses(req, where_clauses, params)

        where_clause = " AND ".join(where_clauses) if where_clauses else "TRUE"

        count_query = """
        SELECT COUNT(*) as count
        FROM langchain_pg_embedding e
        JOIN langchain_pg_collection c ON e.collection_id = c.uuid
        WHERE {}
        """.format(where_clause)

        try:
            results = self._execute_query(count_query, params)
            count = results[0]['count'] if results else 0
            logger.debug(f"文档计数结果: {count}, 索引: {req.index_name}")
            return count
        except Exception as e:
            if "does not exist" in str(e):
                logger.debug(f"索引不存在: {req.index_name}")
                return 0
            logger.error(f"文档计数失败: {e}, 索引: {req.index_name}")
            raise

    def delete_index(self, req: IndexDeleteRequest):
        """删除指定的索引"""
        logger.info(f"删除索引: {req.index_name}")
        try:
            query = "DELETE FROM langchain_pg_collection WHERE name = %(collection_name)s"
            self._execute_query(query, {'collection_name': req.index_name})
            logger.info(f"索引删除成功: {req.index_name}")
        except Exception as e:
            if "does not exist" in str(e):
                logger.debug(f"索引不存在: {req.index_name}")
            else:
                logger.error(f"索引删除失败: {e}")
                raise

    def _build_document_list_query(self, req: DocumentListRequest, where_clause: str, params: Dict[str, Any]) -> str:
        """构建文档列表查询SQL"""
        # 构建排序子句
        sort_order = req.sort_order.upper() if req.sort_order else "DESC"
        if sort_order not in ["ASC", "DESC"]:
            sort_order = "DESC"

        if req.sort_field:
            order_clause = f"ORDER BY (e.cmetadata->>'{req.sort_field}')::timestamp {sort_order}"
        else:
            order_clause = f"ORDER BY (e.cmetadata->>'created_time')::timestamp {sort_order}"

        # 分页参数
        limit_clause = ""
        if req.page > 0 and req.size > 0:
            offset = (req.page - 1) * req.size
            params['limit'] = req.size
            params['offset'] = offset
            limit_clause = "LIMIT %(limit)s OFFSET %(offset)s"

        # 构建完整查询
        return f"""
        SELECT e.id, e.document, e.cmetadata,
               COALESCE(qa_stats.qa_count, 0) as qa_count
        FROM langchain_pg_embedding e
        JOIN langchain_pg_collection c ON e.collection_id = c.uuid
        LEFT JOIN (
            SELECT qa.cmetadata->>'base_chunk_id' as base_chunk_id,
                   COUNT(*) as qa_count
            FROM langchain_pg_embedding qa
            WHERE qa.cmetadata->>'base_chunk_id' IS NOT NULL 
              AND qa.cmetadata->>'base_chunk_id' != ''
              AND qa.cmetadata ? 'qa_answer'
            GROUP BY qa.cmetadata->>'base_chunk_id'
        ) qa_stats ON qa_stats.base_chunk_id = e.id::text
        WHERE {where_clause}
        {order_clause}
        {limit_clause}
        """

    def list_index_document(self, req: DocumentListRequest) -> List[Document]:
        """列出索引中符合条件的文档"""
        where_clauses = []
        params = {}

        where_clauses.append("c.name = %(index_name)s")
        params['index_name'] = req.index_name

        if req.metadata_filter:
            metadata_condition = self._build_metadata_filter(
                req.metadata_filter, params)
            if metadata_condition:
                where_clauses.append(metadata_condition)

        if req.query:
            where_clauses.append("e.document ILIKE %(query_pattern)s")
            params['query_pattern'] = f"%{req.query}%"

        where_clause = " AND ".join(where_clauses) if where_clauses else "TRUE"
        query = self._build_document_list_query(req, where_clause, params)

        try:
            results = self._execute_query(query, params)
            documents = []

            for result in results:
                metadata = result['cmetadata'] if isinstance(
                    result['cmetadata'], dict) else {}
                metadata.update({
                    'chunk_id': result['id'],
                    'qa_count': result['qa_count']
                })

                documents.append(Document(
                    id=result['id'],
                    page_content=result['document'],
                    metadata=metadata
                ))

            page_info = f" (分页: {req.page}/{req.size})" if req.page > 0 and req.size > 0 else " (全部)"
            logger.debug(f"文档列表查询完成, 返回: {len(documents)}个{page_info}")
            return documents

        except Exception as e:
            if "does not exist" in str(e):
                logger.debug(f"索引不存在: {req.index_name}")
                return []
            logger.error(f"文档列表查询失败: {e}")
            raise

    def _handle_qa_records(self, chunk_ids: List[str], keep_qa: bool) -> None:
        """处理QA记录"""
        if keep_qa:
            # 更新关联QA记录的base_chunk_id为空
            query = """
                UPDATE langchain_pg_embedding 
                SET cmetadata = jsonb_set(cmetadata, '{base_chunk_id}', '""'::jsonb)
                WHERE cmetadata->>'base_chunk_id' = ANY(%(chunk_ids)s)
            """
            self._execute_query(query, {'chunk_ids': chunk_ids})
            logger.debug("已更新关联QA记录的base_chunk_id")
        else:
            # 删除关联的QA记录
            query = """
                DELETE FROM langchain_pg_embedding 
                WHERE cmetadata->>'base_chunk_id' = ANY(%(chunk_ids)s)
            """
            self._execute_query(query, {'chunk_ids': chunk_ids})
            logger.debug("已删除关联QA记录")

    def delete_document(self, req: DocumentDeleteRequest) -> None:
        """删除文档记录"""
        chunk_ids = self._collect_target_chunk_ids(
            req.chunk_ids, req.knowledge_ids)

        if not chunk_ids:
            logger.warning("未找到要删除的文档")
            return

        logger.info(
            f"开始删除文档，chunk数量: {len(chunk_ids)}, keep_qa: {req.keep_qa}")

        try:
            # 处理关联的QA记录
            self._handle_qa_records(chunk_ids, req.keep_qa)

            # 删除主文档
            query = "DELETE FROM langchain_pg_embedding WHERE id = ANY(%(chunk_ids)s)"
            self._execute_query(query, {'chunk_ids': chunk_ids})
            logger.info(f"文档删除成功，删除记录: {len(chunk_ids)}个")
        except Exception as e:
            logger.error(f"文档删除失败: {e}")
            raise

    def ingest(self, req: DocumentIngestRequest) -> List[str]:
        """将文档导入到索引中"""
        logger.info(
            f"文档导入开始, 索引: {req.index_name}, 模式: {req.index_mode}, 文档数: {len(req.docs)}")

        if req.index_mode == 'overwrite':
            query = "DELETE FROM langchain_pg_collection WHERE name = %(index_name)s"
            self._execute_query(query, {'index_name': req.index_name})
            logger.info(f"覆盖模式，清理现有数据: {req.index_name}")

        embedding = EmbedBuilder.get_embed(
            req.embed_model_base_url,
            req.embed_model_name,
            req.embed_model_api_key,
            req.embed_model_base_url
        )

        vector_store = PGVector(
            embeddings=embedding,
            collection_name=req.index_name,
            connection=core_settings.db_uri,
            use_jsonb=True,
        )

        try:
            chunk_ids = [doc.metadata["chunk_id"] for doc in req.docs]
            vector_store.add_documents(req.docs, ids=chunk_ids)
            logger.info(f"文档导入成功, 索引: {req.index_name}, 导入数量: {len(req.docs)}")
            return chunk_ids
        except Exception as e:
            logger.error(f"文档导入失败: {e}")
            raise

    def search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """搜索符合条件的文档"""
        logger.info(
            f"文档搜索开始, 索引: {req.index_name}, naive_rag: {req.enable_naive_rag}, qa_rag: {req.enable_qa_rag}")

        results = []

        if req.enable_naive_rag:
            naive_results = self._search_by_type(req, 'naive')
            results.extend(naive_results)

        if req.enable_qa_rag:
            qa_results = self._search_by_type(req, 'qa')
            results.extend(qa_results)

        logger.info(f"文档搜索完成, 索引: {req.index_name}, 结果数: {len(results)}")
        return results

    def _search_by_type(self, req: DocumentRetrieverRequest, rag_type: str) -> List[Document]:
        """按类型执行搜索"""
        logger.debug(f"执行{rag_type}RAG搜索, 索引: {req.index_name}")

        search_req = copy.deepcopy(req)
        search_req.metadata_filter = search_req.metadata_filter or {}

        if rag_type == 'naive':
            search_req.metadata_filter['qa_answer__missing'] = True
        elif rag_type == 'qa':
            search_req.metadata_filter['qa_answer__exists'] = True
            search_req.k = req.qa_size

        try:
            results = self._perform_search(search_req)
            results = self._process_search_results(results, req, rag_type)
            logger.debug(f"{rag_type}RAG搜索完成, 结果数: {len(results)}")
            return results
        except Exception as e:
            logger.error(f"{rag_type}RAG搜索失败: {e}")
            return []

    def _process_search_results(self, results: List[Document], req: DocumentRetrieverRequest, rag_type: str) -> List[Document]:
        """处理搜索结果"""
        # 清理和添加QA答案
        for doc in results:
            for field in ['embedding', 'vector']:
                if field in doc.metadata:
                    del doc.metadata[field]
            if 'qa_answer' in doc.metadata:
                doc.page_content += f"\n{doc.metadata['qa_answer']}"

        # 重排序处理
        if req.enable_rerank and results:
            results = self._rerank_results(req, results)
            if rag_type == 'naive':
                results = self.process_recall_stage(req, results)

        return results

    def _perform_search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """执行向量搜索"""
        try:
            req.validate_search_params()

            embedding = EmbedBuilder.get_embed(
                req.embed_model_base_url,
                req.embed_model_name,
                req.embed_model_api_key,
                req.embed_model_base_url
            )

            vector_store = PGVector(
                embeddings=embedding,
                collection_name=req.index_name,
                connection=core_settings.db_uri,
                use_jsonb=True,
            )

            search_kwargs = {"k": req.k}
            if req.metadata_filter:
                pgvector_filter = self._convert_metadata_filter(
                    req.metadata_filter)
                if pgvector_filter:
                    search_kwargs["filter"] = pgvector_filter

            # 执行搜索
            if req.search_type == "mmr":
                search_kwargs.update({
                    "fetch_k": req.get_effective_fetch_k(),
                    "lambda_mult": req.lambda_mult
                })
                results = vector_store.max_marginal_relevance_search(
                    req.search_query, **search_kwargs)
                # MMR搜索设置默认相似度分数
                for doc in results:
                    if not hasattr(doc, 'metadata'):
                        doc.metadata = {}
                    doc.metadata['similarity_score'] = 1.0
            else:
                # 默认使用相似度阈值搜索
                results_with_scores = vector_store.similarity_search_with_relevance_scores(
                    req.search_query, k=req.k, score_threshold=req.score_threshold or 0.0
                )
                results = []
                for doc, score in results_with_scores:
                    if not hasattr(doc, 'metadata'):
                        doc.metadata = {}
                    doc.metadata['similarity_score'] = float(score)
                    results.append(doc)

            # 添加搜索元数据
            for i, doc in enumerate(results):
                if not hasattr(doc, 'metadata'):
                    doc.metadata = {}
                doc.metadata.update({
                    'search_type': req.search_type,
                    'rank': i + 1,
                    'index_name': req.index_name
                })

            logger.debug(f"向量搜索完成, 结果数: {len(results)}, 类型: {req.search_type}")
            return results

        except Exception as e:
            logger.error(f"向量搜索失败: {e}")
            return []

    def _convert_metadata_filter(self, metadata_filter: dict) -> dict:
        """将内部元数据过滤格式转换为pgvector支持的格式"""
        if not metadata_filter:
            return {}

        pgvector_filter = {}
        for key, value in metadata_filter.items():
            if key.endswith("__exists"):
                field = key.replace("__exists", "")
                pgvector_filter[field] = {"$ne": None}
            elif key.endswith("__missing"):
                field = key.replace("__missing", "")
                pgvector_filter[field] = {"$eq": None}
            elif key.endswith("__like"):
                field = key.replace("__like", "")
                pgvector_filter[field] = {"$like": value}
            elif key.endswith("__ilike"):
                field = key.replace("__ilike", "")
                pgvector_filter[field] = {"$ilike": value}
            else:
                pgvector_filter[key] = {"$eq": value}

        return pgvector_filter

    def _rerank_results(self, req: DocumentRetrieverRequest, results: List[Document]) -> List[Document]:
        """重排序处理"""
        if not results:
            return results

        logger.debug(f"重排序开始, 原始: {len(results)}, 目标: {req.rerank_top_k}")

        reranked_results = ReRankManager.rerank_documents(
            rerank_model_base_url=req.rerank_model_base_url,
            rerank_model_name=req.rerank_model_name,
            rerank_model_api_key=req.rerank_model_api_key,
            search_query=req.search_query,
            search_result=results,
            rerank_top_k=req.rerank_top_k,
        )

        logger.debug(f"重排序完成, 结果数: {len(reranked_results)}")
        return reranked_results

    def process_recall_stage(self, req: DocumentRetrieverRequest, results: List[Document]) -> List[Document]:
        """处理检索阶段，根据不同的召回模式处理搜索结果"""
        recall_mode = req.rag_recall_mode
        logger.debug(f"召回处理开始, 模式: {recall_mode}, 输入: {len(results)}")

        try:
            strategy = RecallStrategyFactory.get_strategy(recall_mode)
            processed_results = strategy.process_recall(req, results, None)
            logger.debug(
                f"召回处理完成, 模式: {recall_mode}, 输出: {len(processed_results)}")
            return processed_results
        except ValueError as e:
            logger.warning(f"召回策略'{recall_mode}'不存在: {e}, 使用默认策略'chunk'")
            default_strategy = RecallStrategyFactory.get_strategy('chunk')
            processed_results = default_strategy.process_recall(
                req, results, None)
            logger.debug(f"默认召回处理完成, 输出: {len(processed_results)}")
            return processed_results
