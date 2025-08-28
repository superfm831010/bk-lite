import copy
import json
from typing import List, Dict, Any, Optional
from collections import defaultdict

import psycopg
from langchain_core.documents import Document
from langchain_postgres import PGVector
from sanic.log import logger

from src.core.embed.embed_builder import EmbedBuilder
from src.core.rerank.rerank_manager import ReRankManager
from src.core.sanic_plus.env.core_settings import core_settings
from src.core.sanic_plus.utils.timing_decorator import timeit
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

    def ensure_fulltext_index(self) -> None:
        """确保全文检索索引存在，提高全文搜索性能"""
        try:
            # 创建GIN索引来优化全文检索性能
            create_index_query = """
                CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_langchain_pg_embedding_fulltext 
                ON langchain_pg_embedding 
                USING GIN (to_tsvector('simple', document))
            """

            logger.info("开始创建全文检索索引...")
            self._execute_query(create_index_query)
            logger.info("全文检索索引创建完成")

        except Exception as e:
            # 索引创建失败不应该影响正常功能
            logger.warning(f"全文检索索引创建失败（不影响功能）: {e}")

    def _rrf(self, results: List[List[str]], rank_const: int = 1, min_score: float = 0) -> tuple[List[str], List[float]]:
        """Reciprocal Rank Fusion算法实现"""
        scores: Dict[str, float] = defaultdict(float)
        for result in results:
            for i, doc_id in enumerate(result):
                scores[doc_id] += 1 / (i + rank_const)

        scored_items = list(scores.items())
        scored_items.sort(reverse=True, key=lambda x: x[1])

        sorted_ids = [item[0] for item in scored_items]
        sorted_scores = [item[1] for item in scored_items]

        # 过滤低分结果
        filtered_results = [(doc_id, score) for doc_id, score in zip(
            sorted_ids, sorted_scores) if score >= min_score]

        if filtered_results:
            filtered_ids, filtered_scores = zip(*filtered_results)
            return list(filtered_ids), list(filtered_scores)
        else:
            return [], []

    @timeit("全文搜索")
    def _fulltext_search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """执行PostgreSQL全文检索（使用tsvector和tsquery）"""
        try:
            where_clauses = []
            params = {}

            # 构建基础查询条件
            where_clauses.append("c.name = %(index_name)s")
            params['index_name'] = req.index_name

            # 添加元数据过滤
            if req.metadata_filter:
                metadata_condition = self._build_metadata_filter(
                    req.metadata_filter, params)
                if metadata_condition:
                    where_clauses.append(metadata_condition)

            # 预处理搜索查询：清理特殊字符，准备用于全文检索
            search_query = req.search_query.strip()
            # 移除可能导致tsquery语法错误的特殊字符
            cleaned_query = search_query.replace("'", "").replace(
                '"', '').replace('&', ' ').replace('|', ' ').replace('!', ' ')
            # 将多个空格合并为单个空格
            cleaned_query = ' '.join(cleaned_query.split())

            if not cleaned_query:
                logger.warning(f"全文搜索跳过 - 原因: 查询词为空")
                return []

            # 使用PostgreSQL全文检索
            # to_tsvector: 将文档转换为tsvector格式（支持中英文）
            # to_tsquery: 将查询转换为tsquery格式
            # ts_rank: 计算相关性分数
            where_clauses.append(
                "to_tsvector('simple', e.document) @@ to_tsquery('simple', %(search_tsquery)s)")

            # 构建tsquery：将搜索词用&连接（AND操作）
            query_terms = cleaned_query.split()
            tsquery_parts = []
            for term in query_terms:
                if term:
                    # 为每个词添加前缀匹配支持（:*表示前缀匹配）
                    tsquery_parts.append(f"'{term}':*")

            if not tsquery_parts:
                logger.warning(f"全文搜索跳过 - 原因: 无有效查询词")
                return []

            params['search_tsquery'] = ' & '.join(tsquery_parts)

            # 构建全文检索查询
            query = f"""
                SELECT e.id, e.document, e.cmetadata,
                       ts_rank(to_tsvector('simple', e.document), to_tsquery('simple', %(search_tsquery)s)) as ts_score,
                       ts_rank_cd(to_tsvector('simple', e.document), to_tsquery('simple', %(search_tsquery)s)) as ts_score_cd
                FROM langchain_pg_embedding e
                JOIN langchain_pg_collection c ON e.collection_id = c.uuid
                WHERE {" AND ".join(where_clauses)}
                ORDER BY 
                    ts_rank_cd(to_tsvector('simple', e.document), to_tsquery('simple', %(search_tsquery)s)) DESC,
                    ts_rank(to_tsvector('simple', e.document), to_tsquery('simple', %(search_tsquery)s)) DESC,
                    LENGTH(e.document) ASC
                LIMIT %(limit)s
            """
            params['limit'] = req.k * 2  # 获取更多候选文档

            logger.debug(
                f"使用全文检索 - 查询词: '{search_query}', tsquery: '{params['search_tsquery']}'")
            logger.debug(f"全文检索SQL: {query}")
            logger.debug(f"全文检索参数: {params}")

            results = self._execute_query(query, params)
            documents = []

            for result in results:
                metadata = result['cmetadata'] if isinstance(
                    result['cmetadata'], dict) else {}

                ts_score = float(result['ts_score']
                                 ) if result['ts_score'] else 0.0
                ts_score_cd = float(
                    result['ts_score_cd']) if result['ts_score_cd'] else 0.0

                # 使用ts_rank_cd作为主要分数，ts_rank作为辅助分数
                # 归一化为0.3-1.0范围，确保不会被阈值过滤且低于向量搜索分数
                final_score = max(ts_score_cd, ts_score)
                normalized_score = min(
                    0.3 + final_score * 0.7, 1.0) if final_score > 0 else 0.3

                metadata.update({
                    'ts_score': ts_score,
                    'ts_score_cd': ts_score_cd,
                    'similarity_score': normalized_score,
                    'search_method': 'fulltext'
                })

                documents.append(Document(
                    id=result['id'],
                    page_content=result['document'],
                    metadata=metadata
                ))

            logger.debug(
                f"全文检索完成 - 索引: {req.index_name}, 查询: '{search_query}', 结果数: {len(documents)}")
            return documents

        except Exception as e:
            logger.error(
                f"全文检索异常 - 索引: {req.index_name}, 查询: '{req.search_query}', 错误: {e}")
            # 降级为ILIKE搜索
            logger.info(f"降级为ILIKE搜索 - 索引: {req.index_name}")
            return self._fallback_ilike_search(req)

    def _fallback_ilike_search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """降级的ILIKE模糊搜索实现"""
        try:
            where_clauses = []
            params = {}

            # 构建基础查询条件
            where_clauses.append("c.name = %(index_name)s")
            params['index_name'] = req.index_name

            # 添加元数据过滤
            if req.metadata_filter:
                metadata_condition = self._build_metadata_filter(
                    req.metadata_filter, params)
                if metadata_condition:
                    where_clauses.append(metadata_condition)

            # 使用ILIKE模糊搜索
            search_query = req.search_query.strip()
            where_clauses.append("e.document ILIKE %(search_pattern)s")
            params['search_pattern'] = f"%{search_query}%"

            # 构建模糊搜索查询
            query = f"""
                SELECT e.id, e.document, e.cmetadata,
                       1.0 as fallback_score
                FROM langchain_pg_embedding e
                JOIN langchain_pg_collection c ON e.collection_id = c.uuid
                WHERE {" AND ".join(where_clauses)}
                ORDER BY 
                    CASE 
                        WHEN e.document ILIKE %(exact_pattern)s THEN 1
                        WHEN LOWER(e.document) LIKE LOWER(%(search_pattern)s) THEN 2
                        ELSE 3
                    END,
                    LENGTH(e.document) ASC
                LIMIT %(limit)s
            """
            params['exact_pattern'] = f"%{search_query}%"
            params['limit'] = req.k * 2

            logger.debug(f"降级ILIKE搜索 - 查询词: '{search_query}'")

            results = self._execute_query(query, params)
            documents = []

            for result in results:
                metadata = result['cmetadata'] if isinstance(
                    result['cmetadata'], dict) else {}
                fallback_score = float(result['fallback_score'])
                metadata.update({
                    'fallback_score': fallback_score,
                    'similarity_score': 0.3,  # 降级搜索使用较低的固定分数
                    'search_method': 'ilike_fallback'
                })

                documents.append(Document(
                    id=result['id'],
                    page_content=result['document'],
                    metadata=metadata
                ))

            logger.info(
                f"降级ILIKE搜索完成 - 索引: {req.index_name}, 结果数: {len(documents)}")
            return documents

        except Exception as e:
            logger.error(
                f"降级ILIKE搜索异常 - 索引: {req.index_name}, 错误: {e}")
            return []

    def _get_psycopg_uri(self) -> str:
        """将SQLAlchemy格式的URI转换为psycopg支持的格式"""
        uri = core_settings.db_uri
        # 移除SQLAlchemy方言前缀，如 postgresql+psycopg:// -> postgresql://
        if uri.startswith('postgresql+psycopg://'):
            uri = uri.replace('postgresql+psycopg://', 'postgresql://')
        elif uri.startswith('postgres+psycopg://'):
            uri = uri.replace('postgres+psycopg://', 'postgresql://')
        return uri

    @timeit("SQL更新执行")
    def _execute_update_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """执行UPDATE/DELETE等非查询SQL，返回影响的行数"""
        try:
            with psycopg.connect(self._get_psycopg_uri()) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params or {})
                    affected_rows = cur.rowcount
                    conn.commit()

                    # 记录影响行数
                    param_keys = list(params.keys()) if params else []
                    logger.info(
                        f"SQL更新详情 - 影响行数: {affected_rows}, 参数键: {param_keys}")
                    return affected_rows
        except Exception as e:
            # 隐藏敏感参数，只记录参数键名
            param_keys = list(params.keys()) if params else []
            logger.error(f"SQL更新异常详情 - 参数键: {param_keys}")
            raise

    @timeit("SQL查询执行")
    def _execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """执行SQL查询"""
        try:
            with psycopg.connect(self._get_psycopg_uri()) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params or {})
                    conn.commit()

                    result_count = 0
                    if cur.description:
                        columns = [desc[0] for desc in cur.description]
                        results = [dict(zip(columns, row))
                                   for row in cur.fetchall()]
                        result_count = len(results)
                    else:
                        results = []

                    # 记录查询结果数
                    param_keys = list(params.keys()) if params else []
                    logger.info(
                        f"SQL查询详情 - 结果数: {result_count}, 参数键: {param_keys}")
                    return results
        except Exception as e:
            param_keys = list(params.keys()) if params else []
            logger.error(f"SQL查询异常详情 - 参数键: {param_keys}")
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
            elif key.endswith("__not_blank"):
                field_key = key.replace("__not_blank", "")
                conditions.append(
                    f"(e.cmetadata ? %(metadata_{field_key}_not_blank_exists)s AND TRIM(e.cmetadata->>%(metadata_{field_key}_not_blank_field)s) != '')")
                params[f"metadata_{field_key}_not_blank_exists"] = field_key
                params[f"metadata_{field_key}_not_blank_field"] = field_key
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

    @timeit("元数据更新")
    def update_metadata(self, req: DocumentMetadataUpdateRequest) -> None:
        """更新文档元数据"""
        chunk_ids = self._collect_target_chunk_ids(
            req.chunk_ids, req.knowledge_ids)

        if not chunk_ids:
            logger.info("元数据更新跳过 - 原因: 未找到匹配的文档")
            return

        logger.info(f"元数据更新开始 - 目标chunks: {len(chunk_ids)}")

        # 验证要更新的记录是否存在
        check_query = """
            SELECT id FROM langchain_pg_embedding 
            WHERE id = ANY(%(chunk_ids)s)
        """
        existing_records = self._execute_query(
            check_query, {'chunk_ids': chunk_ids})
        existing_ids = [record['id'] for record in existing_records]

        if not existing_ids:
            logger.warning(f"元数据更新失败 - 原因: 指定chunks不存在, 数量: {len(chunk_ids)}")
            return

        if len(existing_ids) != len(chunk_ids):
            missing_count = len(chunk_ids) - len(existing_ids)
            logger.warning(f"元数据更新部分失败 - 缺失chunks: {missing_count}个")

        query = """
            UPDATE langchain_pg_embedding 
            SET cmetadata = cmetadata || %(new_metadata)s::jsonb
            WHERE id = ANY(%(chunk_ids)s)
        """
        params = {
            'new_metadata': json.dumps(req.metadata),
            'chunk_ids': existing_ids
        }

        try:
            affected_rows = self._execute_update_query(query, params)

            if affected_rows > 0:
                logger.info(f"元数据更新详情 - 更新数量: {affected_rows}")
            else:
                logger.warning("元数据更新无效果 - 可能原因: 数据无变化")
        except Exception as e:
            logger.error(f"元数据更新异常详情 - 错误: {e}")
            raise

    @timeit("文档计数")
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
            logger.info(f"文档计数详情 - 索引: {req.index_name}, 文档数: {count}")
            return count
        except Exception as e:
            if "does not exist" in str(e):
                logger.info(f"文档计数详情 - 索引: {req.index_name}, 文档数: 0 (索引不存在)")
                return 0
            logger.error(f"文档计数异常 - 索引: {req.index_name}")
            raise

    @timeit("索引删除")
    def delete_index(self, req: IndexDeleteRequest):
        """删除指定的索引"""
        logger.info(f"索引删除开始 - 索引: {req.index_name}")

        try:
            query = "DELETE FROM langchain_pg_collection WHERE name = %(collection_name)s"
            affected_rows = self._execute_update_query(
                query, {'collection_name': req.index_name})

            if affected_rows > 0:
                logger.info(
                    f"索引删除详情 - 索引: {req.index_name}, 清理记录: {affected_rows}")
            else:
                logger.info(f"索引删除详情 - 索引: {req.index_name} (索引不存在)")
        except Exception as e:
            if "does not exist" in str(e):
                logger.info(f"索引删除详情 - 索引: {req.index_name} (索引不存在)")
            else:
                logger.error(f"索引删除异常 - 索引: {req.index_name}")
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

    @timeit("文档列表查询")
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

            page_info = f" (分页: {req.page}/{req.size})" if req.page > 0 and req.size > 0 else ""
            logger.info(
                f"文档列表查询完成 - 索引: {req.index_name}, 返回: {len(documents)}个{page_info}")
            return documents

        except Exception as e:
            if "does not exist" in str(e):
                logger.info(
                    f"文档列表查询完成 - 索引: {req.index_name}, 返回: 0个 (索引不存在)")
                return []
            logger.error(
                f"文档列表查询失败 - 索引: {req.index_name}, 错误: {e}")
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
            affected_rows = self._execute_update_query(
                query, {'chunk_ids': chunk_ids})
            if affected_rows > 0:
                logger.info(f"QA记录保留处理完成 - 更新关联: {affected_rows}个")
        else:
            # 删除关联的QA记录
            query = """
                DELETE FROM langchain_pg_embedding 
                WHERE cmetadata->>'base_chunk_id' = ANY(%(chunk_ids)s)
            """
            affected_rows = self._execute_update_query(
                query, {'chunk_ids': chunk_ids})
            if affected_rows > 0:
                logger.info(f"QA记录清理完成 - 删除: {affected_rows}个")

    @timeit("文档删除")
    def delete_document(self, req: DocumentDeleteRequest) -> None:
        """删除文档记录"""
        chunk_ids = self._collect_target_chunk_ids(
            req.chunk_ids, req.knowledge_ids)

        if not chunk_ids:
            logger.info("文档删除跳过 - 原因: 未找到匹配的文档")
            return

        logger.info(
            f"文档删除开始 - 目标chunks: {len(chunk_ids)}, 保留QA: {req.keep_qa}")

        try:
            # 处理关联的QA记录
            self._handle_qa_records(chunk_ids, req.keep_qa)

            # 删除主文档
            query = "DELETE FROM langchain_pg_embedding WHERE id = ANY(%(chunk_ids)s)"
            affected_rows = self._execute_update_query(
                query, {'chunk_ids': chunk_ids})

            logger.info(f"文档删除成功 - 删除数量: {affected_rows}")
        except Exception as e:
            logger.error(f"文档删除失败 - 错误: {e}")
            raise

    @timeit("文档导入")
    def ingest(self, req: DocumentIngestRequest) -> List[str]:
        """将文档导入到索引中"""
        logger.info(
            f"文档导入开始 - 索引: {req.index_name}, 模式: {req.index_mode}, 文档数: {len(req.docs)}")

        if req.index_mode == 'overwrite':
            query = "DELETE FROM langchain_pg_collection WHERE name = %(index_name)s"
            affected_rows = self._execute_update_query(
                query, {'index_name': req.index_name})
            logger.info(
                f"覆盖模式清理完成 - 索引: {req.index_name}, 清理记录: {affected_rows}")

        # 确保全文检索索引存在（仅在首次导入时尝试创建）
        try:
            self.ensure_fulltext_index()
        except Exception as e:
            logger.warning(f"全文检索索引创建跳过: {e}")

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

            logger.info(
                f"文档导入成功 - 索引: {req.index_name}, 导入数量: {len(req.docs)}")
            return chunk_ids
        except Exception as e:
            logger.error(
                f"文档导入失败 - 索引: {req.index_name}, 错误: {e}")
            raise

    @timeit("文档搜索")
    def search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """搜索符合条件的文档"""
        logger.info(
            f"文档搜索开始 - 索引: {req.index_name}, naive_rag: {req.enable_naive_rag}, qa_rag: {req.enable_qa_rag}")

        results = []

        if req.enable_naive_rag:
            naive_results = self._search_by_type(req, 'naive')
            results.extend(naive_results)

        if req.enable_qa_rag:
            qa_results = self._search_by_type(req, 'qa')
            results.extend(qa_results)

        logger.info(
            f"文档搜索完成 - 索引: {req.index_name}, 结果数: {len(results)}")
        return results

    @timeit("分类搜索")
    def _search_by_type(self, req: DocumentRetrieverRequest, rag_type: str) -> List[Document]:
        """按类型执行搜索"""
        logger.debug(f"搜索执行开始 - 类型: {rag_type}, 索引: {req.index_name}")

        search_req = copy.deepcopy(req)
        search_req.metadata_filter = search_req.metadata_filter or {}

        if rag_type == 'naive':
            search_req.metadata_filter['is_doc'] = "1"
        elif rag_type == 'qa':
            search_req.metadata_filter['is_doc'] = "0"
            search_req.k = req.qa_size

        try:
            results = self._perform_search(search_req)
            results = self._process_search_results(results, req, rag_type)

            logger.debug(
                f"搜索执行完成 - 类型: {rag_type}, 结果数: {len(results)}")
            return results
        except Exception as e:
            logger.error(
                f"搜索执行失败 - 类型: {rag_type}, 错误: {e}")
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

    @timeit("向量搜索")
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
                # HybridSearch: 结合向量搜索和全文搜索，各占一定比例
                # 计算各自应该返回的文档数量（确保均衡分配，各占约50%）
                vector_k = max(1, req.k // 2)  # 向量搜索部分：至少1个，通常占一半
                fulltext_k = max(1, req.k - vector_k)  # 全文搜索部分：占剩余部分

                logger.info(
                    f"HybridSearch: vector_k={vector_k}, fulltext_k={fulltext_k}, total_k={req.k}")

                # 1. 执行向量搜索（多取一些候选，提高质量）
                vector_results_with_scores = vector_store.similarity_search_with_relevance_scores(
                    req.search_query, k=vector_k * 2, score_threshold=req.score_threshold or 0.0,
                    filter=search_kwargs.get("filter")
                )
                vector_results = []
                vector_doc_ids = []
                for doc, score in vector_results_with_scores:
                    if not hasattr(doc, 'metadata'):
                        doc.metadata = {}
                    doc.metadata['similarity_score'] = float(score)
                    doc.metadata['search_method'] = 'vector'
                    vector_results.append(doc)
                    vector_doc_ids.append(str(doc.metadata.get(
                        'chunk_id', doc.id if hasattr(doc, 'id') else str(id(doc)))))

                # 2. 执行全文搜索（调整k值以获取相应比例的结果）
                fulltext_req = copy.deepcopy(req)
                fulltext_req.k = fulltext_k * 2  # 多取一些候选，提高质量
                fulltext_results = self._fulltext_search(fulltext_req)
                fulltext_doc_ids = []
                for doc in fulltext_results:
                    fulltext_doc_ids.append(str(doc.metadata.get(
                        'chunk_id', doc.id if hasattr(doc, 'id') else str(id(doc)))))

                # 3. 使用RRF合并结果，确保各自的比例贡献
                if vector_doc_ids or fulltext_doc_ids:
                    rrf_input = []

                    # 限制各自的贡献数量，确保比例平衡
                    if vector_doc_ids:
                        # 只取前vector_k个向量搜索结果参与RRF
                        rrf_input.append(vector_doc_ids[:vector_k])
                    if fulltext_doc_ids:
                        # 只取前fulltext_k个全文搜索结果参与RRF
                        rrf_input.append(fulltext_doc_ids[:fulltext_k])

                    merged_doc_ids, rrf_scores = self._rrf(
                        rrf_input, rank_const=1, min_score=0)

                    # 4. 构建合并后的文档映射
                    all_docs = {}
                    for doc in vector_results:
                        doc_id = str(doc.metadata.get(
                            'chunk_id', doc.id if hasattr(doc, 'id') else str(id(doc))))
                        all_docs[doc_id] = doc
                    for doc in fulltext_results:
                        doc_id = str(doc.metadata.get(
                            'chunk_id', doc.id if hasattr(doc, 'id') else str(id(doc))))
                        if doc_id not in all_docs:  # 避免重复
                            all_docs[doc_id] = doc

                    # 5. 按RRF分数排序并构建最终结果
                    results = []
                    for i, (doc_id, rrf_score) in enumerate(zip(merged_doc_ids[:req.k], rrf_scores[:req.k])):
                        if doc_id in all_docs:
                            doc = all_docs[doc_id]
                            if not hasattr(doc, 'metadata'):
                                doc.metadata = {}

                            # 保留原有的similarity_score，如果没有则设置为0.0
                            if 'similarity_score' not in doc.metadata:
                                doc.metadata['similarity_score'] = 0.0

                            doc.metadata['rrf_score'] = float(rrf_score)
                            doc.metadata['hybrid_rank'] = i + 1
                            results.append(doc)
                else:
                    results = []

            # 添加搜索元数据
            for i, doc in enumerate(results):
                if not hasattr(doc, 'metadata'):
                    doc.metadata = {}
                doc.metadata.update({
                    'search_type': req.search_type,
                    'rank': i + 1,
                    'index_name': req.index_name
                })

            return results

        except Exception as e:
            logger.error(f"向量搜索异常 - 索引: {req.index_name}, 错误: {e}")
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
            elif key.endswith("__not_blank"):
                field = key.replace("__not_blank", "")
                pgvector_filter[field] = {"$ne": ""}
            else:
                pgvector_filter[key] = {"$eq": value}

        return pgvector_filter

    @timeit("重排序")
    def _rerank_results(self, req: DocumentRetrieverRequest, results: List[Document]) -> List[Document]:
        """重排序处理"""
        if not results:
            return results

        reranked_results = ReRankManager.rerank_documents(
            rerank_model_base_url=req.rerank_model_base_url,
            rerank_model_name=req.rerank_model_name,
            rerank_model_api_key=req.rerank_model_api_key,
            search_query=req.search_query,
            search_result=results,
            rerank_top_k=req.rerank_top_k,
        )

        logger.debug(
            f"重排序完成 - 输入: {len(results)}, 输出: {len(reranked_results)}")
        return reranked_results

    @timeit("召回处理")
    def process_recall_stage(self, req: DocumentRetrieverRequest, results: List[Document]) -> List[Document]:
        """处理检索阶段，根据不同的召回模式处理搜索结果"""
        recall_mode = req.rag_recall_mode

        try:
            strategy = RecallStrategyFactory.get_strategy(recall_mode)
            processed_results = strategy.process_recall(req, results, None)

            logger.debug(
                f"召回处理完成 - 模式: {recall_mode}, 输入: {len(results)}, 输出: {len(processed_results)}")
            return processed_results
        except ValueError as e:
            logger.warning(f"召回策略异常 - 模式: '{recall_mode}' 不存在, 使用默认策略 'chunk'")
            default_strategy = RecallStrategyFactory.get_strategy('chunk')
            processed_results = default_strategy.process_recall(
                req, results, None)

            logger.debug(
                f"默认召回处理完成 - 输入: {len(results)}, 输出: {len(processed_results)}")
            return processed_results
