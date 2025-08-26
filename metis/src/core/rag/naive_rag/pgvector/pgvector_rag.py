import copy
import json
from typing import List, Dict, Any
from urllib.parse import urlparse
import psycopg

from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import DistanceStrategy
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
from src.core.rag.naive_rag.pgvector.pgvector_query_builder import PgvectorQueryBuilder
from src.core.rag.naive_rag.recall_strategies.recall_strategy_factory import RecallStrategyFactory
from src.core.rag.naive_rag.pgvector.pgvector_config import PgvectorConfig


class PgvectorRag(BaseRag):
    """PostgreSQL + pgvector RAG 实现类"""

    def __init__(self, config: PgvectorConfig = None):
        """
        初始化 PostgreSQL 连接

        Args:
            config: pgvector配置，如果为None则使用默认配置
        """
        self.config = config or PgvectorConfig.get_default_config()
        self.config.validate()
        self._init_connection()

    def _init_connection(self):
        """初始化数据库连接"""
        try:
            # 解析数据库 URI
            self.db_uri = core_settings.db_uri
            if not self.db_uri:
                raise ValueError(
                    "Database URI not configured in core_settings.db_uri")

            # 解析连接信息
            parsed = urlparse(self.db_uri)
            self.connection_kwargs = {
                "host": parsed.hostname,
                "port": parsed.port or 5432,
                "dbname": parsed.path.lstrip('/') if parsed.path else 'postgres',
                "user": parsed.username,
                "password": parsed.password,
            }

            # 测试连接并确保 pgvector 扩展已启用
            self._ensure_pgvector_extension()

        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL connection: {e}")
            raise

    def _ensure_pgvector_extension(self):
        """确保 pgvector 扩展已启用并优化索引设置"""
        try:
            with psycopg.connect(**self.connection_kwargs) as conn:
                with conn.cursor() as cur:
                    # 检查并创建 pgvector 扩展
                    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

                    # 如果启用了HNSW索引优化，设置相关参数
                    if self.config.enable_hnsw_index:
                        # 设置HNSW索引参数
                        cur.execute(
                            f"SET hnsw.ef_construction = {self.config.hnsw_ef_construction};")
                        logger.debug(
                            f"设置HNSW ef_construction参数: {self.config.hnsw_ef_construction}")

                    conn.commit()
                    logger.debug("pgvector extension ensured and optimized")
        except Exception as e:
            logger.error(f"Failed to ensure pgvector extension: {e}")
            raise

    def _optimize_table_indices(self, table_name: str):
        """
        优化表的索引设置以提升查询性能

        Args:
            table_name: 表名
        """
        try:
            with psycopg.connect(**self.connection_kwargs) as conn:
                with conn.cursor() as cur:
                    # 检查表是否存在
                    cur.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = %s
                        );
                    """, (table_name,))

                    if not cur.fetchone()[0]:
                        logger.debug(f"表 {table_name} 不存在，跳过索引优化")
                        return

                    # 如果启用了HNSW索引，创建向量索引
                    if self.config.enable_hnsw_index:
                        index_name = f"{table_name}_embedding_hnsw_idx"

                        # 检查索引是否已存在
                        cur.execute("""
                            SELECT EXISTS (
                                SELECT FROM pg_class c 
                                JOIN pg_namespace n ON n.oid = c.relnamespace 
                                WHERE c.relname = %s
                            );
                        """, (index_name,))

                        if not cur.fetchone()[0]:
                            # 创建HNSW索引
                            create_index_sql = f"""
                            CREATE INDEX CONCURRENTLY {index_name} 
                            ON {table_name} USING hnsw (embedding vector_cosine_ops) 
                            WITH (m = {self.config.hnsw_m}, ef_construction = {self.config.hnsw_ef_construction});
                            """
                            cur.execute(create_index_sql)
                            logger.debug(f"创建HNSW索引: {index_name}")

                    # 创建元数据GIN索引（如果不存在）
                    metadata_index_name = f"{table_name}_cmetadata_gin_idx"
                    cur.execute("""
                        SELECT EXISTS (
                            SELECT FROM pg_class c 
                            JOIN pg_namespace n ON n.oid = c.relnamespace 
                            WHERE c.relname = %s
                        );
                    """, (metadata_index_name,))

                    if not cur.fetchone()[0]:
                        create_gin_index_sql = f"""
                        CREATE INDEX CONCURRENTLY {metadata_index_name} 
                        ON {table_name} USING gin (cmetadata jsonb_path_ops);
                        """
                        cur.execute(create_gin_index_sql)
                        logger.debug(f"创建元数据GIN索引: {metadata_index_name}")

                    conn.commit()

        except Exception as e:
            logger.warning(f"索引优化失败 {table_name}: {e}")
            # 索引优化失败不应该影响主要功能，所以只记录警告

    def _get_connection_string(self) -> str:
        """获取数据库连接字符串"""
        return self.db_uri

    def _execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict]:
        """执行 SQL 查询"""
        try:
            with psycopg.connect(**self.connection_kwargs) as conn:
                with conn.cursor() as cur:
                    print(query)
                    if params:
                        cur.execute(query, params)
                    else:
                        cur.execute(query)

                    if cur.description:
                        columns = [desc[0] for desc in cur.description]
                        results = []
                        for row in cur.fetchall():
                            result = dict(zip(columns, row))
                            results.append(result)
                        return results
                    return []
        except Exception as e:
            logger.error(
                f"Failed to execute query: {e}\nQuery: {query}\nParams: {params}")
            raise

    def update_metadata(self, req: DocumentMetadataUpdateRequest):
        """
        根据过滤条件更新文档的元数据

        Args:
            req: 包含索引名称、元数据过滤条件和新元数据的请求对象
        """
        table_name = PgvectorQueryBuilder.TABLE_NAME
        collection_table = PgvectorQueryBuilder.COLLECTION_TABLE

        # 构建过滤条件，特殊处理 chunk_id（对应表的主键 id）
        where_clauses = []
        params = {}

        # 添加 index_name 过滤条件（通过 collection 表的 name 字段）
        where_clauses.append(f"c.name = %(index_name)s")
        params['index_name'] = req.index_name

        # 检查是否包含 chunk_id，如果有则作为主键 id 处理
        if 'chunk_id' in req.metadata_filter:
            chunk_id = req.metadata_filter.pop(
                'chunk_id')  # 从 metadata_filter 中移除
            if isinstance(chunk_id, list):
                # 支持批量更新多个 chunk_id
                where_clauses.append("e.id = ANY(%(chunk_ids)s)")
                params['chunk_ids'] = chunk_id
            else:
                # 单个 chunk_id
                where_clauses.append("e.id = %(chunk_id)s")
                params['chunk_id'] = chunk_id

        # 处理其他元数据过滤条件
        if req.metadata_filter:
            metadata_where, metadata_params = PgvectorQueryBuilder.build_metadata_filter(
                req.metadata_filter)
            if metadata_where != "TRUE":
                # 将 cmetadata 引用替换为表别名
                metadata_where = metadata_where.replace(
                    "cmetadata", "e.cmetadata")
                where_clauses.append(metadata_where)
            params.update(metadata_params)

        # 如果没有任何过滤条件，则不执行更新
        if len(where_clauses) <= 1:  # 只有 index_name 条件
            logger.warning("No filter conditions provided for metadata update")
            return

        where_clause = " AND ".join(where_clauses)

        # 构建更新的 JSON 合并操作
        metadata_json = json.dumps(req.metadata)

        # 使用 IN 子查询来更新
        update_query = f"""
        UPDATE {table_name}
        SET cmetadata = cmetadata || %(new_metadata)s::jsonb
        WHERE id IN (
            SELECT e.id 
            FROM {table_name} e
            JOIN {collection_table} c ON e.collection_id = c.uuid
            WHERE {where_clause}
        )
        """

        params['new_metadata'] = metadata_json

        logger.debug(f"Executing update query: {update_query}")
        logger.debug(f"Update parameters: {params}")
        self._execute_query(update_query, params)
        logger.debug(
            f"Updated metadata for documents in index {req.index_name}")

    def count_index_document(self, req: DocumentCountRequest) -> int:
        """
        统计索引中符合条件的文档数量

        Args:
            req: 文档计数请求对象

        Returns:
            符合条件的文档数量
        """
        table_name = PgvectorQueryBuilder.TABLE_NAME
        collection_table = PgvectorQueryBuilder.COLLECTION_TABLE

        # 构建查询条件
        where_clauses = []
        params = {}

        # 添加 index_name 过滤条件（通过 collection 表的 name 字段）
        where_clauses.append(f"c.name = %(index_name)s")
        params['index_name'] = req.index_name

        # 检查是否包含 chunk_id，如果有则作为主键 id 处理
        metadata_filter = req.metadata_filter.copy()  # 创建副本避免修改原始数据
        if 'chunk_id' in metadata_filter:
            chunk_id = metadata_filter.pop('chunk_id')
            if isinstance(chunk_id, list):
                where_clauses.append("e.id = ANY(%(chunk_ids)s)")
                params['chunk_ids'] = chunk_id
            else:
                where_clauses.append("e.id = %(chunk_id)s")
                params['chunk_id'] = chunk_id

        # 添加元数据过滤条件
        if metadata_filter:
            metadata_where, metadata_params = PgvectorQueryBuilder.build_metadata_filter(
                metadata_filter)
            if metadata_where != "TRUE":
                # 将 cmetadata 引用替换为表别名
                metadata_where = metadata_where.replace(
                    "cmetadata", "e.cmetadata")
                where_clauses.append(metadata_where)
            params.update(metadata_params)

        # 添加文本匹配条件
        if req.query:
            where_clauses.append("e.document ILIKE %(query_pattern)s")
            params['query_pattern'] = f"%{req.query}%"

        where_clause = " AND ".join(where_clauses) if where_clauses else "TRUE"

        # 构建带 JOIN 的统计查询
        count_query = f"""
        SELECT COUNT(*) as count
        FROM {table_name} e
        JOIN {collection_table} c ON e.collection_id = c.uuid
        WHERE {where_clause}
        """

        try:
            results = self._execute_query(count_query, params)
            return results[0]['count'] if results else 0
        except Exception as e:
            # 如果表不存在，返回 0
            if "does not exist" in str(e):
                return 0
            raise

    def delete_index(self, req: IndexDeleteRequest):
        """
        删除指定的索引（删除集合记录，级联删除所有相关数据）

        Args:
            req: 包含索引名称的请求对象
        """
        try:
            # 直接删除集合记录，由于有 ON DELETE CASCADE 约束，
            # 会自动删除 langchain_pg_embedding 表中的相关记录
            delete_collection_query = f"DELETE FROM {PgvectorQueryBuilder.COLLECTION_TABLE} WHERE name = %(collection_name)s"
            self._execute_query(delete_collection_query, {
                                'collection_name': req.index_name})
            logger.debug(
                f"Deleted collection {req.index_name} and all related embeddings (cascaded)")

        except Exception as e:
            # 如果表不存在或其他错误，记录日志但不抛出异常
            if "does not exist" in str(e):
                logger.debug(
                    f"Index {req.index_name} does not exist, nothing to delete")
            else:
                logger.error(f"Failed to delete index {req.index_name}: {e}")
                raise

    def list_index_document(self, req: DocumentListRequest) -> List[Document]:
        """
        列出索引中符合条件的文档

        Args:
            req: 包含索引名称、页码、大小和过滤条件的请求对象

        Returns:
            文档列表
        """
        table_name = PgvectorQueryBuilder.TABLE_NAME
        collection_table = PgvectorQueryBuilder.COLLECTION_TABLE

        # 构建查询条件
        where_clauses = []
        params = {}

        # 添加 index_name 过滤条件（通过 collection 表的 name 字段）
        where_clauses.append(f"c.name = %(index_name)s")
        params['index_name'] = req.index_name

        # 检查是否包含 chunk_id，如果有则作为主键 id 处理
        metadata_filter = req.metadata_filter.copy()  # 创建副本避免修改原始数据
        if 'chunk_id' in metadata_filter:
            chunk_id = metadata_filter.pop('chunk_id')
            if isinstance(chunk_id, list):
                where_clauses.append("e.id = ANY(%(chunk_ids)s)")
                params['chunk_ids'] = chunk_id
            else:
                where_clauses.append("e.id = %(chunk_id)s")
                params['chunk_id'] = chunk_id

        # 添加元数据过滤条件
        if metadata_filter:
            metadata_where, metadata_params = PgvectorQueryBuilder.build_metadata_filter(
                metadata_filter)
            if metadata_where != "TRUE":
                # 将 cmetadata 引用替换为表别名
                metadata_where = metadata_where.replace(
                    "cmetadata", "e.cmetadata")
                where_clauses.append(metadata_where)
            params.update(metadata_params)

        # 添加文本匹配条件
        if req.query:
            where_clauses.append("e.document ILIKE %(query_pattern)s")
            params['query_pattern'] = f"%{req.query}%"

        where_clause = " AND ".join(where_clauses) if where_clauses else "TRUE"

        # 计算偏移量
        offset = (req.page - 1) * req.size if req.page > 0 else 0

        # 构建排序条件
        order_clause = "ORDER BY e.id DESC"  # 默认排序
        if req.sort_field and req.sort_order:
            sort_order = req.sort_order.lower()
            if sort_order not in ['asc', 'desc']:
                sort_order = 'desc'

            # 处理 metadata.xxx 格式的排序字段
            if req.sort_field.startswith('metadata.'):
                # 提取 metadata. 后面的字段名
                actual_field = req.sort_field[9:]  # 去掉 'metadata.' 前缀
                if actual_field in ['created_time', 'updated_time']:
                    order_clause = f"ORDER BY (e.cmetadata->>'{actual_field}')::timestamp {sort_order} NULLS LAST"
                else:
                    order_clause = f"ORDER BY e.cmetadata->>'{actual_field}' {sort_order} NULLS LAST"
            elif req.sort_field in ['created_time', 'updated_time']:
                order_clause = f"ORDER BY (e.cmetadata->>'{req.sort_field}')::timestamp {sort_order} NULLS LAST"
            else:
                order_clause = f"ORDER BY e.cmetadata->>'{req.sort_field}' {sort_order} NULLS LAST"

        # 构建带 JOIN 的查询
        list_query = f"""
        SELECT e.id, e.document, e.cmetadata
        FROM {table_name} e
        JOIN {collection_table} c ON e.collection_id = c.uuid
        WHERE {where_clause}
        {order_clause}
        LIMIT %(limit)s OFFSET %(offset)s
        """

        params.update({
            'limit': req.size,
            'offset': offset
        })

        logger.debug(f"查询文档列表，排序字段: {req.sort_field}, 排序方式: {req.sort_order}")

        try:
            results = self._execute_query(list_query, params)
            documents = []
            for result in results:
                metadata = result['cmetadata'] if isinstance(
                    result['cmetadata'], dict) else {}
                # 用数据库的 id 覆盖 metadata 中的 chunk_id
                if 'chunk_id' in metadata:
                    metadata['chunk_id'] = result['id']
                # 创建 Document 对象，设置 id 为数据库中的真实 id
                documents.append(
                    Document(
                        id=result['id'],
                        page_content=result['document'],
                        metadata=metadata
                    )
                )
            return documents
        except Exception as e:
            # 如果表不存在，返回空列表
            if "does not exist" in str(e):
                return []
            raise

    def delete_document(self, req: DocumentDeleteRequest):
        """
        删除符合条件的文档

        Args:
            req: 包含索引名称和过滤条件的请求对象
        """
        table_name = PgvectorQueryBuilder.TABLE_NAME
        collection_table = PgvectorQueryBuilder.COLLECTION_TABLE

        # 构建过滤条件，特殊处理 chunk_id（对应表的主键 id）
        where_clauses = []
        params = {}

        # 添加 index_name 过滤条件（通过 collection 表的 name 字段）
        where_clauses.append(f"c.name = %(index_name)s")
        params['index_name'] = req.index_name

        # 检查是否包含 chunk_id，如果有则作为主键 id 处理
        if 'chunk_id' in req.metadata_filter:
            chunk_id = req.metadata_filter.pop(
                'chunk_id')  # 从 metadata_filter 中移除
            if isinstance(chunk_id, list):
                # 支持批量删除多个 chunk_id
                where_clauses.append("e.id = ANY(%(chunk_ids)s)")
                params['chunk_ids'] = chunk_id
            else:
                # 单个 chunk_id
                where_clauses.append("e.id = %(chunk_id)s")
                params['chunk_id'] = chunk_id

        # 处理其他元数据过滤条件
        if req.metadata_filter:
            metadata_where, metadata_params = PgvectorQueryBuilder.build_metadata_filter(
                req.metadata_filter)
            if metadata_where != "TRUE":
                # 将 cmetadata 引用替换为表别名
                metadata_where = metadata_where.replace(
                    "cmetadata", "e.cmetadata")
                where_clauses.append(metadata_where)
            params.update(metadata_params)

        # 如果没有任何过滤条件，则不执行删除
        if len(where_clauses) <= 1:  # 只有 index_name 条件
            logger.warning(
                "No filter conditions provided for document deletion")
            return

        where_clause = " AND ".join(where_clauses)

        # 使用 IN 子查询来删除
        delete_query = f"""
        DELETE FROM {table_name} 
        WHERE id IN (
            SELECT e.id 
            FROM {table_name} e
            JOIN {collection_table} c ON e.collection_id = c.uuid
            WHERE {where_clause}
        )
        """
        logger.debug(f"Executing delete query: {delete_query}")
        logger.debug(f"Delete parameters: {params}")
        self._execute_query(delete_query, params)
        logger.debug(f"Deleted documents from index {req.index_name}")

    def ingest(self, req: DocumentIngestRequest) -> List[str]:
        """
        将文档导入到索引中，并返回插入的文档ID列表

        Args:
            req: 包含索引名称、文档和嵌入模型信息的请求对象

        Returns:
            插入的文档ID列表（对应数据库中的主键ID）
        """
        # 如果是覆盖模式，先删除集合中的所有数据
        if req.index_mode == 'overwrite':
            try:
                # 获取集合ID
                collection_query, collection_params = PgvectorQueryBuilder.get_collection_id_query(
                    req.index_name)
                collection_results = self._execute_query(
                    collection_query, collection_params)

                if collection_results:
                    collection_id = collection_results[0]['uuid']

                    # 删除主数据表中属于该集合的记录
                    delete_query = f"DELETE FROM {PgvectorQueryBuilder.TABLE_NAME} WHERE collection_id = %(collection_id)s"
                    self._execute_query(
                        delete_query, {'collection_id': collection_id})
                    logger.debug(
                        f"Deleted existing data in collection {req.index_name} for overwrite mode")
                else:
                    logger.debug(
                        f"Collection {req.index_name} not found, nothing to delete for overwrite mode")

            except Exception as e:
                logger.warning(
                    f"Failed to delete existing data for collection {req.index_name}: {e}")

        # 获取嵌入模型
        embedding = EmbedBuilder.get_embed(
            req.embed_model_base_url,
            req.embed_model_name,
            req.embed_model_api_key,
            req.embed_model_base_url
        )

        # 优化的批量插入处理
        try:
            if req.docs:
                inserted_ids = self._batch_insert_documents(
                    req.docs, req.index_name, embedding)

                # 存储完成后优化索引（异步执行，不阻塞主流程）
                try:
                    self._optimize_table_indices(
                        PgvectorQueryBuilder.TABLE_NAME)
                except Exception as e:
                    logger.warning(f"索引优化失败，但不影响数据存储: {e}")

                logger.debug(
                    f"Successfully ingested {len(req.docs)} documents to index {req.index_name}, "
                    f"返回 {len(inserted_ids)} 个文档ID")
                return inserted_ids
        except Exception as e:
            logger.error(f"Failed to ingest documents: {e}")
            raise

        return []

    def _batch_insert_documents(self, docs: List[Document], index_name: str, embedding) -> List[str]:
        """
        批量插入文档并返回插入的ID列表，优化性能

        Args:
            docs: 要插入的文档列表
            index_name: 索引名称
            embedding: 嵌入模型

        Returns:
            插入的文档ID列表
        """
        inserted_ids = []
        batch_size = self.config.batch_size  # 使用配置的批处理大小
        total_docs = len(docs)

        logger.debug(f"开始批量插入 {total_docs} 个文档，批次大小: {batch_size}")

        # 使用 PGVector 进行批量插入
        vector_store = PGVector(
            embeddings=embedding,
            collection_name=index_name,
            connection=self._get_connection_string(),
            distance_strategy=DistanceStrategy.COSINE,
            use_jsonb=True,
        )

        # 处理批次插入，增加重试机制
        for i in range(0, total_docs, batch_size):
            batch_docs = docs[i:i + batch_size]
            batch_start = i + 1
            batch_end = min(i + batch_size, total_docs)

            logger.debug(f"处理批次 {batch_start}-{batch_end}/{total_docs}")

            # 重试机制
            retry_count = 0
            while retry_count <= self.config.max_retries:
                try:
                    # 添加文档，langchain-postgres 的 add_documents 方法会返回ID列表
                    batch_ids = vector_store.add_documents(batch_docs)
                    if batch_ids:
                        inserted_ids.extend(batch_ids)
                        logger.debug(
                            f"批次 {batch_start}-{batch_end} 插入成功，获得 {len(batch_ids)} 个ID")
                    else:
                        # 如果 add_documents 不返回ID，则使用自定义方法获取最新插入的ID
                        batch_ids = self._get_latest_inserted_ids(
                            index_name, len(batch_docs))
                        inserted_ids.extend(batch_ids)
                        logger.debug(
                            f"批次 {batch_start}-{batch_end} 插入成功，通过查询获得 {len(batch_ids)} 个ID")
                    break  # 成功则跳出重试循环

                except Exception as e:
                    retry_count += 1
                    if retry_count > self.config.max_retries:
                        logger.error(
                            f"批次 {batch_start}-{batch_end} 插入失败，已重试 {retry_count-1} 次: {e}")
                        raise
                    else:
                        logger.warning(
                            f"批次 {batch_start}-{batch_end} 插入失败，第 {retry_count} 次重试: {e}")
                        import time
                        time.sleep(self.config.retry_delay)

            logger.debug(f"批次 {batch_start}-{batch_end} 处理完成")

        return inserted_ids

    def _get_latest_inserted_ids(self, index_name: str, count: int) -> List[str]:
        """
        获取最新插入的文档ID列表（当 add_documents 不返回ID时的备用方案）

        Args:
            index_name: 索引名称
            count: 需要获取的ID数量

        Returns:
            最新插入的ID列表
        """
        try:
            # 获取集合ID
            collection_query, collection_params = PgvectorQueryBuilder.get_collection_id_query(
                index_name)
            collection_results = self._execute_query(
                collection_query, collection_params)

            if not collection_results:
                logger.warning(f"未找到集合 {index_name}")
                return []

            collection_id = collection_results[0]['uuid']

            # 查询最新插入的文档ID
            query = f"""
            SELECT id 
            FROM {PgvectorQueryBuilder.TABLE_NAME} 
            WHERE collection_id = %(collection_id)s 
            ORDER BY id DESC 
            LIMIT %(limit)s
            """

            params = {
                'collection_id': collection_id,
                'limit': count
            }

            results = self._execute_query(query, params)
            return [result['id'] for result in results]

        except Exception as e:
            logger.error(f"获取最新插入ID失败: {e}")
            return []

    def search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """
        搜索符合条件的文档

        Args:
            req: 检索请求对象

        Returns:
            检索到的文档列表
        """
        search_result = []

        # 检查是否启用了特定的 RAG 类型，如果没有则默认使用 naive RAG
        enable_naive_rag = getattr(req, 'enable_naive_rag', True)
        enable_qa_rag = getattr(req, 'enable_qa_rag', False)

        logger.debug(
            f"RAG搜索配置 - naive: {enable_naive_rag}, qa: {enable_qa_rag}")

        if enable_naive_rag:
            naive_results = self._execute_rag_search(req, 'naive')
            search_result.extend(naive_results)
            logger.debug(f"naive RAG 返回 {len(naive_results)} 个结果")

        if enable_qa_rag:
            qa_results = self._execute_rag_search(req, 'qa')
            search_result.extend(qa_results)
            logger.debug(f"qa RAG 返回 {len(qa_results)} 个结果")

        # 如果两种 RAG 都没有启用，默认使用 naive RAG
        if not enable_naive_rag and not enable_qa_rag:
            logger.debug("未指定RAG类型，默认使用 naive RAG")
            naive_results = self._execute_rag_search(req, 'naive')
            search_result.extend(naive_results)

        logger.debug(f"总共返回 {len(search_result)} 个搜索结果")
        return search_result

    def _execute_rag_search(self, req: DocumentRetrieverRequest, rag_type: str) -> List[Document]:
        """执行RAG搜索的通用方法，简化版本"""
        rag_request = copy.deepcopy(req)

        # 根据RAG类型设置过滤条件
        if rag_type == 'naive':
            # naive RAG: 优先搜索原始文档内容
            rag_request.metadata_filter = rag_request.metadata_filter or {}
            rag_request.metadata_filter['qa_answer__missing'] = True
        elif rag_type == 'qa':
            # qa RAG: 搜索包含QA答案的文档
            rag_request.metadata_filter = rag_request.metadata_filter or {}
            rag_request.metadata_filter['qa_answer__exists'] = True

        logger.debug(f"RAG搜索类型: {rag_type}")

        try:
            # 简化搜索逻辑
            if req.enable_vector_search and req.enable_term_search:
                search_results = self._hybrid_search(rag_request)
            elif req.enable_vector_search:
                search_results = self._vector_search(rag_request)
            elif req.enable_term_search:
                search_results = self._text_search(rag_request)
            else:
                logger.warning("向量搜索和文本搜索都未启用")
                return []

            # 如果naive RAG没有结果，尝试搜索所有文档
            if rag_type == 'naive' and not search_results:
                logger.debug("naive RAG无结果，移除qa_answer过滤条件重新搜索")
                fallback_request = copy.deepcopy(req)
                if 'qa_answer__missing' in fallback_request.metadata_filter:
                    del fallback_request.metadata_filter['qa_answer__missing']

                if req.enable_vector_search and req.enable_term_search:
                    search_results = self._hybrid_search(fallback_request)
                elif req.enable_vector_search:
                    search_results = self._vector_search(fallback_request)
                elif req.enable_term_search:
                    search_results = self._text_search(fallback_request)

            # 处理搜索结果
            search_results = self._process_search_result(search_results)

            # 重排序和召回处理
            if req.enable_rerank:
                search_results = self._rerank_results(req, search_results)
                if rag_type == 'naive':  # 只有naive RAG需要召回阶段处理
                    search_results = self.process_recall_stage(
                        req, search_results)

            logger.debug(f"RAG搜索 {rag_type} 最终返回 {len(search_results)} 个结果")
            return search_results

        except Exception as e:
            logger.error(f"RAG搜索失败: {e}")
            return []

    def _hybrid_search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """
        执行混合搜索：结合向量搜索和文本搜索的结果，简化版本

        Args:
            req: 检索请求对象

        Returns:
            混合搜索结果列表
        """
        # 简化权重参数
        vector_weight = getattr(req, 'vector_search_weight', 0.6)  # 向量搜索权重稍高
        text_weight = getattr(req, 'text_search_weight', 0.4)

        # 简化候选数量计算
        num_candidates = req.rag_k
        vector_candidates = max(1, int(num_candidates * 0.6))
        text_candidates = max(1, int(num_candidates * 0.4))

        logger.debug(
            f"混合搜索 - 向量候选: {vector_candidates}, 文本候选: {text_candidates}")

        try:
            vector_results = []
            text_results = []

            # 执行向量搜索
            if vector_weight > 0:
                vector_req = copy.deepcopy(req)
                vector_req.rag_k = vector_candidates
                vector_results = self._vector_search(vector_req)

            # 执行文本搜索
            if text_weight > 0:
                text_req = copy.deepcopy(req)
                text_req.rag_k = text_candidates
                text_results = self._text_search(text_req)

            # 简化合并逻辑
            return self._merge_search_results(vector_results, text_results, vector_weight, text_weight, req.rag_k)

        except Exception as e:
            logger.error(f"混合搜索失败: {e}")
            return []

    def _vector_search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """
        执行向量搜索

        Args:
            req: 检索请求对象

        Returns:
            向量搜索结果列表
        """
        try:
            # 获取嵌入模型
            embedding = EmbedBuilder.get_embed(
                req.embed_model_base_url,
                req.embed_model_name,
                req.embed_model_api_key,
                req.embed_model_base_url
            )

            # 使用 PGVector 进行搜索
            vector_store = PGVector(
                embeddings=embedding,
                collection_name=req.index_name,
                connection=self._get_connection_string(),
                distance_strategy=DistanceStrategy.COSINE,
                use_jsonb=True,
            )

            # 构建搜索参数
            search_kwargs = {"k": req.rag_k}

            # 添加元数据过滤
            if req.metadata_filter:
                search_kwargs["filter"] = req.metadata_filter

            # 执行向量搜索
            search_results = vector_store.similarity_search(
                req.search_query,
                **search_kwargs
            )

            # 为结果添加搜索类型标记和分数
            for i, doc in enumerate(search_results):
                if not hasattr(doc, 'metadata'):
                    doc.metadata = {}
                doc.metadata['search_type'] = 'vector'
                doc.metadata['vector_rank'] = i + 1

            return search_results

        except Exception as e:
            logger.error(f"向量搜索失败: {e}")
            return []

    def _merge_search_results(self, vector_results: List[Document], text_results: List[Document],
                              vector_weight: float, text_weight: float, top_k: int) -> List[Document]:
        """
        合并向量搜索和文本搜索的结果，简化版本

        Args:
            vector_results: 向量搜索结果
            text_results: 文本搜索结果
            vector_weight: 向量搜索权重
            text_weight: 文本搜索权重
            top_k: 返回的结果数量

        Returns:
            合并后的搜索结果
        """
        # 使用文档内容哈希去重
        doc_scores = {}

        # 处理向量搜索结果
        for i, doc in enumerate(vector_results):
            content_hash = hash(doc.page_content)
            vector_score = (len(vector_results) - i) / \
                len(vector_results) if vector_results else 0

            if content_hash not in doc_scores:
                doc_scores[content_hash] = {
                    'document': doc,
                    'vector_score': vector_score,
                    'text_score': 0.0
                }
            else:
                doc_scores[content_hash]['vector_score'] = max(
                    doc_scores[content_hash]['vector_score'], vector_score
                )

        # 处理文本搜索结果
        for i, doc in enumerate(text_results):
            content_hash = hash(doc.page_content)
            text_score = (len(text_results) - i) / \
                len(text_results) if text_results else 0

            if content_hash not in doc_scores:
                doc_scores[content_hash] = {
                    'document': doc,
                    'vector_score': 0.0,
                    'text_score': text_score
                }
            else:
                doc_scores[content_hash]['text_score'] = max(
                    doc_scores[content_hash]['text_score'], text_score
                )

        # 计算综合分数并排序
        scored_docs = []
        for doc_info in doc_scores.values():
            combined_score = (doc_info['vector_score'] * vector_weight +
                              doc_info['text_score'] * text_weight)

            doc = doc_info['document']
            if not hasattr(doc, 'metadata'):
                doc.metadata = {}

            doc.metadata.update({
                'combined_score': combined_score,
                'vector_score': doc_info['vector_score'],
                'text_score': doc_info['text_score']
            })

            scored_docs.append((combined_score, doc))

        # 按分数降序排序并返回前 top_k 个结果
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        merged_results = [doc for _, doc in scored_docs[:top_k]]

        logger.debug(f"合并结果: 向量{len(vector_results)}个, 文本{len(text_results)}个, "
                     f"去重后{len(doc_scores)}个, 最终返回{len(merged_results)}个")

        return merged_results

    def _detect_search_language(self, query: str) -> str:
        """
        检测搜索查询的语言，优化为中文场景优先

        Args:
            query: 搜索查询字符串

        Returns:
            语言代码：'chinese', 'english'
        """
        if not query:
            return 'chinese'  # 默认中文场景

        # 检查是否包含中文字符
        chinese_char_count = sum(
            1 for char in query if '\u4e00' <= char <= '\u9fff')

        # 只要包含中文字符就认为是中文查询
        return 'chinese' if chinese_char_count > 0 else 'english'

    def _text_search(self, req: DocumentRetrieverRequest) -> List[Document]:
        """执行优化的文本搜索，简化为中文场景优先"""
        table_name = PgvectorQueryBuilder.TABLE_NAME
        collection_table = PgvectorQueryBuilder.COLLECTION_TABLE

        # 构建文本搜索查询
        where_clauses = []
        params = {'search_query': req.search_query}

        # 添加 index_name 过滤条件
        where_clauses.append(f"c.name = %(index_name)s")
        params['index_name'] = req.index_name

        # 处理 chunk_id 过滤
        metadata_filter = req.metadata_filter.copy()
        if 'chunk_id' in metadata_filter:
            chunk_id = metadata_filter.pop('chunk_id')
            if isinstance(chunk_id, list):
                where_clauses.append("e.id = ANY(%(chunk_ids)s)")
                params['chunk_ids'] = chunk_id
            else:
                where_clauses.append("e.id = %(chunk_id)s")
                params['chunk_id'] = chunk_id

        # 添加元数据过滤
        if metadata_filter:
            metadata_where, metadata_params = PgvectorQueryBuilder.build_metadata_filter(
                metadata_filter)
            if metadata_where != "TRUE":
                metadata_where = metadata_where.replace(
                    "cmetadata", "e.cmetadata")
                where_clauses.append(metadata_where)
            params.update(metadata_params)

        # 简化文本搜索逻辑：优先中文ILIKE搜索
        text_search_mode = getattr(req, 'text_search_mode', 'match')
        search_language = self._detect_search_language(req.search_query)

        if text_search_mode == 'exact':
            # 精确搜索
            text_search_clause = """
            (e.document = %(search_query)s 
             OR e.cmetadata->>'knowledge_title' = %(search_query)s)
            """
            order_clause = "ORDER BY e.id DESC"
        else:
            # 默认模糊搜索，适合中文场景
            text_search_clause = """
            (e.document ILIKE %(like_pattern)s 
             OR e.cmetadata->>'knowledge_title' ILIKE %(like_pattern)s)
            """
            params['like_pattern'] = f"%{req.search_query}%"

            # 中文优先的排序逻辑
            order_clause = """
            ORDER BY 
                CASE 
                    WHEN e.document ILIKE %(like_pattern)s THEN 1
                    WHEN e.cmetadata->>'knowledge_title' ILIKE %(like_pattern)s THEN 2
                    ELSE 3
                END,
                LENGTH(e.document) ASC,
                e.id DESC
            """

        where_clauses.append(text_search_clause)
        where_clause = " AND ".join(where_clauses)

        search_query = f"""
        SELECT e.id, e.document, e.cmetadata
        FROM {table_name} e
        JOIN {collection_table} c ON e.collection_id = c.uuid
        WHERE {where_clause}
        {order_clause}
        LIMIT %(limit)s
        """

        params['limit'] = req.rag_k

        try:
            logger.debug(
                f"执行文本搜索，模式: {text_search_mode}, 查询: '{req.search_query}'")
            results = self._execute_query(search_query, params)
            documents = []

            for i, result in enumerate(results):
                metadata = result['cmetadata'] if isinstance(
                    result['cmetadata'], dict) else {}
                metadata.update({
                    'search_type': 'text',
                    'text_rank': i + 1,
                    'search_mode': text_search_mode,
                    'chunk_id': result['id']
                })

                documents.append(Document(
                    id=result['id'],
                    page_content=result['document'],
                    metadata=metadata
                ))

            logger.debug(f"文本搜索返回 {len(documents)} 个结果")
            return documents

        except Exception as e:
            logger.error(f"文本搜索失败: {e}")
            return []

    def _process_search_result(self, docs: List[Document]) -> List[Document]:
        """处理搜索结果，移除向量字段并添加QA答案"""
        for doc in docs:
            # 移除向量字段（如果存在）
            if 'embedding' in doc.metadata:
                del doc.metadata['embedding']
            if 'vector' in doc.metadata:
                del doc.metadata['vector']

            # 添加QA答案到内容中
            if 'qa_answer' in doc.metadata:
                doc.page_content += f"\n{doc.metadata['qa_answer']}"
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

    def process_recall_stage(self, req: DocumentRetrieverRequest, search_result: List[Document]) -> List[Document]:
        """
        处理检索阶段，根据不同的召回模式处理搜索结果

        Args:
            req: 检索请求对象
            search_result: 初始搜索结果

        Returns:
            处理后的搜索结果
        """
        recall_mode = req.rag_recall_mode

        logger.debug(f"处理召回阶段，召回模式: {recall_mode}")

        try:
            strategy = RecallStrategyFactory.get_strategy(recall_mode)
            # 传递适当的客户端参数，对于不需要客户端的策略传递 None
            return strategy.process_recall(req, search_result, None)
        except ValueError as e:
            logger.warning(f"召回策略 '{recall_mode}' 不存在: {e}")
            # 如果策略不存在，回退到默认的chunk模式
            default_strategy = RecallStrategyFactory.get_strategy('chunk')
            return default_strategy.process_recall(req, search_result, None)
