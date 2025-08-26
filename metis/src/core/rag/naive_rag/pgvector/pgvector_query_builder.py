from typing import Dict, List, Any, Tuple
from langchain_openai import OpenAIEmbeddings

from src.core.embed.embed_builder import EmbedBuilder
from src.web.entity.rag.base.document_retriever_request import DocumentRetrieverRequest


class PgvectorQueryBuilder:
    """
    PostgreSQL + pgvector 查询构建器

    数据库表结构：

    langchain_pg_collection:
    - uuid: uuid (主键)
    - name: character varying (唯一约束)
    - cmetadata: json

    langchain_pg_embedding:
    - id: character varying (主键)
    - collection_id: uuid (外键 -> langchain_pg_collection.uuid)
    - embedding: vector (pgvector 类型)
    - document: character varying (文档内容)
    - cmetadata: jsonb (元数据)

    索引：
    - langchain_pg_embedding_pkey: PRIMARY KEY btree (id)
    - ix_cmetadata_gin: gin (cmetadata jsonb_path_ops)
    """

    # 常量定义
    TABLE_NAME = "langchain_pg_embedding"
    COLLECTION_TABLE = "langchain_pg_collection"
    RRF_RANK_CONSTANT = 60  # RRF 算法中的排名常数

    @staticmethod
    def get_table_name(index_name: str = None) -> str:
        """获取表名"""
        return PgvectorQueryBuilder.TABLE_NAME

    @staticmethod
    def get_collection_id_query(collection_name: str) -> Tuple[str, Dict[str, Any]]:
        """构建获取集合ID的查询"""
        sql = f"SELECT uuid FROM {PgvectorQueryBuilder.COLLECTION_TABLE} WHERE name = %(collection_name)s"
        params = {'collection_name': collection_name}
        return sql, params

    @staticmethod
    def build_metadata_filter(metadata_filter: Dict) -> Tuple[str, Dict[str, Any]]:
        """构建元数据过滤条件的 SQL WHERE 子句和参数"""
        if not metadata_filter:
            return "TRUE", {}

        where_clauses = []
        params = {}
        param_counter = 1

        # 操作符映射，减少重复代码
        operators = {
            '__exists': lambda key, _: f"cmetadata->>'{key[:-8]}' IS NOT NULL",
            '__missing': lambda key, _: f"cmetadata->>'{key[:-9]}' IS NULL",
            '__is_null': lambda key, _: f"cmetadata->>'{key[:-8]}' IS NULL",
            '__is_not_null': lambda key, _: f"cmetadata->>'{key[:-12]}' IS NOT NULL",
            '__is_empty': lambda key, _: f"(cmetadata->>'{key[:-9]}' IS NULL OR cmetadata->>'{key[:-9]}' = '')",
            '__is_not_empty': lambda key, _: f"(cmetadata->>'{key[:-14]}' IS NOT NULL AND cmetadata->>'{key[:-14]}' != '')",
        }

        for key, value in metadata_filter.items():
            param_name = f"filter_param_{param_counter}"
            param_counter += 1

            # 处理无参数操作符
            if any(key.endswith(op) for op in operators):
                for op, func in operators.items():
                    if key.endswith(op):
                        where_clauses.append(func(key, value))
                        break
                continue

            # 处理有参数的操作符
            if key.endswith('__range'):
                range_key = key[:-7]
                if isinstance(value, dict) and 'gte' in value and 'lte' in value:
                    gte_param, lte_param = f"{param_name}_gte", f"{param_name}_lte"
                    where_clauses.append(
                        f"(cmetadata->>'{range_key}')::numeric BETWEEN %({gte_param})s AND %({lte_param})s")
                    params.update(
                        {gte_param: value['gte'], lte_param: value['lte']})
                else:
                    raise ValueError(
                        f"Invalid range filter for key {key}: {value}")

            elif key.endswith('__in'):
                in_key = key[:-4]
                if isinstance(value, list):
                    where_clauses.append(
                        f"cmetadata->>'{in_key}' = ANY(%({param_name})s)")
                    params[param_name] = value
                else:
                    raise ValueError(
                        f"Invalid in filter for key {key}: {value}")

            elif key.endswith('__not_in'):
                not_in_key = key[:-8]
                if isinstance(value, list):
                    where_clauses.append(
                        f"cmetadata->>'{not_in_key}' != ALL(%({param_name})s)")
                    params[param_name] = value
                else:
                    raise ValueError(
                        f"Invalid not_in filter for key {key}: {value}")

            elif key.endswith(('__like', '__not_like')):
                is_not = '__not_like' in key
                field_key = key[:-10] if is_not else key[:-6]
                operator = "NOT ILIKE" if is_not else "ILIKE"
                if isinstance(value, str):
                    where_clauses.append(
                        f"cmetadata->>'{field_key}' {operator} %({param_name})s")
                    params[param_name] = f"%{value}%"
                else:
                    raise ValueError(
                        f"Invalid {'not_like' if is_not else 'like'} filter for key {key}: {value}")

            elif isinstance(value, (str, bool, int, float)):
                # 精确匹配
                where_clauses.append(f"cmetadata->>'{key}' = %({param_name})s")
                params[param_name] = str(value)
            else:
                raise ValueError(
                    f"Unsupported metadata filter type for key {key}: {type(value)}")

        where_clause = " AND ".join(where_clauses) if where_clauses else "TRUE"
        return where_clause, params

    @staticmethod
    def build_text_search_clause(req: DocumentRetrieverRequest) -> Tuple[str, Dict[str, Any]]:
        """构建文本搜索条件"""
        if not req.enable_term_search or not req.search_query:
            return "TRUE", {}

        search_clauses = []
        params = {"search_query": req.search_query}

        # 搜索字段定义
        search_fields = ["document", "cmetadata->>'knowledge_title'"]

        if req.text_search_mode == 'match':
            # PostgreSQL 全文搜索
            for field in search_fields:
                if field.startswith("cmetadata"):
                    search_clauses.append(
                        f"to_tsvector('english', {field}) @@ plainto_tsquery('english', %(search_query)s)")
                else:
                    search_clauses.append(
                        f"to_tsvector('english', {field}) @@ plainto_tsquery('english', %(search_query)s)")
        else:
            # ILIKE 搜索（默认和 match_phrase）
            pattern_key = "search_pattern"
            params[pattern_key] = f"%{req.search_query}%"
            for field in search_fields:
                search_clauses.append(f"{field} ILIKE %({pattern_key})s")

        search_clause = "(" + " OR ".join(search_clauses) + ")"
        return search_clause, params

    @staticmethod
    def build_vector_search_clause(req: DocumentRetrieverRequest,
                                   embedding: OpenAIEmbeddings) -> Tuple[str, List[float], Dict[str, Any]]:
        """构建向量搜索条件"""
        if not req.enable_vector_search:
            return "", [], {}

        query_vector = embedding.embed_query(req.search_query)
        order_clause = "embedding <=> %(query_vector)s"
        params = {"query_vector": query_vector}

        return order_clause, query_vector, params

    @staticmethod
    def build_combined_query(req: DocumentRetrieverRequest,
                             collection_id: str = None,
                             limit: int = None) -> Tuple[str, Dict[str, Any]]:
        """构建组合查询（文本 + 向量搜索）"""
        table_name = PgvectorQueryBuilder.TABLE_NAME
        collection_table = PgvectorQueryBuilder.COLLECTION_TABLE

        # 获取嵌入模型
        embedding = EmbedBuilder.get_embed(
            req.embed_model_base_url,
            req.embed_model_name,
            req.embed_model_api_key,
            req.embed_model_base_url
        )

        # 构建基础 WHERE 条件
        metadata_where, metadata_params = PgvectorQueryBuilder.build_metadata_filter(
            req.metadata_filter)
        all_params = metadata_params.copy()

        # 添加集合过滤条件 - 使用 JOIN 方式而不是直接的 collection_id
        where_clauses = []

        # 添加 index_name 过滤条件（通过 collection 表的 name 字段）
        where_clauses.append(f"c.name = %(index_name)s")
        all_params['index_name'] = req.index_name

        # 添加元数据过滤条件
        if metadata_where != "TRUE":
            # 将 cmetadata 引用替换为表别名
            metadata_where = metadata_where.replace("cmetadata", "e.cmetadata")
            where_clauses.append(metadata_where)

        base_where = " AND ".join(where_clauses) if where_clauses else "TRUE"

        # 根据搜索类型构建查询
        search_type = PgvectorQueryBuilder._get_search_type(req)

        if search_type == 'hybrid':
            sql, params = PgvectorQueryBuilder._build_hybrid_search_query_with_join(
                req, table_name, collection_table, base_where, embedding)
        elif search_type == 'vector':
            sql, params = PgvectorQueryBuilder._build_vector_only_query_with_join(
                req, table_name, collection_table, base_where, embedding)
        elif search_type == 'text':
            sql, params = PgvectorQueryBuilder._build_text_only_query_with_join(
                req, table_name, collection_table, base_where)
        else:
            sql, params = PgvectorQueryBuilder._build_metadata_only_query_with_join(
                table_name, collection_table, base_where)

        all_params.update(params)

        # 添加 LIMIT
        limit = limit or getattr(req, 'size', None)
        if limit:
            sql += f" LIMIT %(limit)s"
            all_params['limit'] = limit

        return sql, all_params

    @staticmethod
    def _get_search_type(req: DocumentRetrieverRequest) -> str:
        """确定搜索类型"""
        has_vector = req.enable_vector_search
        has_text = req.enable_term_search and req.search_query

        if has_vector and has_text:
            return 'hybrid'
        elif has_vector:
            return 'vector'
        elif has_text:
            return 'text'
        else:
            return 'metadata_only'

    @staticmethod
    def _build_hybrid_search_query(req: DocumentRetrieverRequest,
                                   table_name: str,
                                   metadata_where: str,
                                   embedding: OpenAIEmbeddings) -> Tuple[str, Dict[str, Any]]:
        """构建混合搜索查询（RRF）"""
        text_clause, text_params = PgvectorQueryBuilder.build_text_search_clause(
            req)
        vector_order, query_vector, vector_params = PgvectorQueryBuilder.build_vector_search_clause(
            req, embedding)

        rrf_constant = PgvectorQueryBuilder.RRF_RANK_CONSTANT

        sql = f"""
        WITH text_search AS (
            SELECT *, 
                   ts_rank(to_tsvector('english', document), plainto_tsquery('english', %(search_query)s)) as text_score,
                   ROW_NUMBER() OVER (ORDER BY ts_rank(to_tsvector('english', document), plainto_tsquery('english', %(search_query)s)) DESC) as text_rank
            FROM {table_name}
            WHERE {metadata_where} AND ({text_clause})
            ORDER BY text_score DESC
            LIMIT %(rag_k)s
        ),
        vector_search AS (
            SELECT *, 
                   1 / (1 + (embedding <=> %(query_vector)s)) as vector_score,
                   ROW_NUMBER() OVER (ORDER BY {vector_order}) as vector_rank
            FROM {table_name}
            WHERE {metadata_where}
            ORDER BY {vector_order}
            LIMIT %(rag_k)s
        ),
        combined_results AS (
            SELECT COALESCE(t.id, v.id) as id,
                   COALESCE(t.document, v.document) as document,
                   COALESCE(t.cmetadata, v.cmetadata) as cmetadata,
                   COALESCE(t.embedding, v.embedding) as embedding,
                   COALESCE(t.text_score, 0) * %(text_search_weight)s as weighted_text_score,
                   COALESCE(v.vector_score, 0) * %(vector_search_weight)s as weighted_vector_score,
                   COALESCE(t.text_rank, 9999) as text_rank,
                   COALESCE(v.vector_rank, 9999) as vector_rank
            FROM text_search t 
            FULL OUTER JOIN vector_search v ON t.id = v.id
        )
        SELECT id, document, cmetadata, embedding,
               (1.0 / ({rrf_constant} + text_rank) + 1.0 / ({rrf_constant} + vector_rank)) as rrf_score,
               weighted_text_score + weighted_vector_score as combined_score
        FROM combined_results
        ORDER BY rrf_score DESC, combined_score DESC
        """

        params = {
            **text_params,
            **vector_params,
            'rag_k': req.rag_k,
            'text_search_weight': req.text_search_weight,
            'vector_search_weight': req.vector_search_weight,
            'search_query': req.search_query
        }

        return sql, params

    @staticmethod
    def _build_vector_only_query(req: DocumentRetrieverRequest,
                                 table_name: str,
                                 metadata_where: str,
                                 embedding: OpenAIEmbeddings) -> Tuple[str, Dict[str, Any]]:
        """构建仅向量搜索查询"""
        vector_order, query_vector, vector_params = PgvectorQueryBuilder.build_vector_search_clause(
            req, embedding)

        sql = f"""
        SELECT id, document, cmetadata, embedding,
               1 / (1 + (embedding <=> %(query_vector)s)) as similarity_score
        FROM {table_name}
        WHERE {metadata_where}
        ORDER BY {vector_order}
        """

        return sql, vector_params

    @staticmethod
    def _build_text_only_query(req: DocumentRetrieverRequest,
                               table_name: str,
                               metadata_where: str) -> Tuple[str, Dict[str, Any]]:
        """构建仅文本搜索查询"""
        text_clause, text_params = PgvectorQueryBuilder.build_text_search_clause(
            req)

        sql = f"""
        SELECT id, document, cmetadata, embedding,
               ts_rank(to_tsvector('english', document), plainto_tsquery('english', %(search_query)s)) as text_score
        FROM {table_name}
        WHERE {metadata_where} AND ({text_clause})
        ORDER BY text_score DESC
        """

        params = {**text_params, 'search_query': req.search_query}
        return sql, params

    @staticmethod
    def _build_hybrid_search_query_with_join(req: DocumentRetrieverRequest,
                                             table_name: str,
                                             collection_table: str,
                                             base_where: str,
                                             embedding: OpenAIEmbeddings) -> Tuple[str, Dict[str, Any]]:
        """构建混合搜索查询（RRF） - 带 JOIN"""
        text_clause, text_params = PgvectorQueryBuilder.build_text_search_clause(
            req)
        vector_order, query_vector, vector_params = PgvectorQueryBuilder.build_vector_search_clause(
            req, embedding)

        # 替换 text_clause 中的字段引用为表别名
        text_clause = text_clause.replace(
            "document", "e.document").replace("cmetadata", "e.cmetadata")
        vector_order = vector_order.replace("embedding", "e.embedding")

        rrf_constant = PgvectorQueryBuilder.RRF_RANK_CONSTANT

        sql = f"""
        WITH text_search AS (
            SELECT e.*, 
                   ts_rank(to_tsvector('english', e.document), plainto_tsquery('english', %(search_query)s)) as text_score,
                   ROW_NUMBER() OVER (ORDER BY ts_rank(to_tsvector('english', e.document), plainto_tsquery('english', %(search_query)s)) DESC) as text_rank
            FROM {table_name} e
            JOIN {collection_table} c ON e.collection_id = c.uuid
            WHERE {base_where} AND ({text_clause})
            ORDER BY text_score DESC
            LIMIT %(rag_k)s
        ),
        vector_search AS (
            SELECT e.*, 
                   1 / (1 + (e.embedding <=> %(query_vector)s)) as vector_score,
                   ROW_NUMBER() OVER (ORDER BY {vector_order}) as vector_rank
            FROM {table_name} e
            JOIN {collection_table} c ON e.collection_id = c.uuid
            WHERE {base_where}
            ORDER BY {vector_order}
            LIMIT %(rag_k)s
        ),
        combined_results AS (
            SELECT COALESCE(t.id, v.id) as id,
                   COALESCE(t.document, v.document) as document,
                   COALESCE(t.cmetadata, v.cmetadata) as cmetadata,
                   COALESCE(t.embedding, v.embedding) as embedding,
                   COALESCE(t.text_score, 0) * %(text_search_weight)s as weighted_text_score,
                   COALESCE(v.vector_score, 0) * %(vector_search_weight)s as weighted_vector_score,
                   COALESCE(t.text_rank, 9999) as text_rank,
                   COALESCE(v.vector_rank, 9999) as vector_rank
            FROM text_search t 
            FULL OUTER JOIN vector_search v ON t.id = v.id
        )
        SELECT id, document, cmetadata, embedding,
               (1.0 / ({rrf_constant} + text_rank) + 1.0 / ({rrf_constant} + vector_rank)) as rrf_score,
               weighted_text_score + weighted_vector_score as combined_score
        FROM combined_results
        ORDER BY rrf_score DESC, combined_score DESC
        """

        params = {
            **text_params,
            **vector_params,
            'rag_k': req.rag_k,
            'text_search_weight': req.text_search_weight,
            'vector_search_weight': req.vector_search_weight,
            'search_query': req.search_query,
            'index_name': req.index_name
        }

        return sql, params

    @staticmethod
    def _build_vector_only_query_with_join(req: DocumentRetrieverRequest,
                                           table_name: str,
                                           collection_table: str,
                                           base_where: str,
                                           embedding: OpenAIEmbeddings) -> Tuple[str, Dict[str, Any]]:
        """构建仅向量搜索查询 - 带 JOIN"""
        vector_order, query_vector, vector_params = PgvectorQueryBuilder.build_vector_search_clause(
            req, embedding)
        vector_order = vector_order.replace("embedding", "e.embedding")

        sql = f"""
        SELECT e.id, e.document, e.cmetadata, e.embedding,
               1 / (1 + (e.embedding <=> %(query_vector)s)) as similarity_score
        FROM {table_name} e
        JOIN {collection_table} c ON e.collection_id = c.uuid
        WHERE {base_where}
        ORDER BY {vector_order}
        """

        params = {**vector_params, 'index_name': req.index_name}
        return sql, params

    @staticmethod
    def _build_text_only_query_with_join(req: DocumentRetrieverRequest,
                                         table_name: str,
                                         collection_table: str,
                                         base_where: str) -> Tuple[str, Dict[str, Any]]:
        """构建仅文本搜索查询 - 带 JOIN"""
        text_clause, text_params = PgvectorQueryBuilder.build_text_search_clause(
            req)
        text_clause = text_clause.replace(
            "document", "e.document").replace("cmetadata", "e.cmetadata")

        sql = f"""
        SELECT e.id, e.document, e.cmetadata, e.embedding,
               ts_rank(to_tsvector('english', e.document), plainto_tsquery('english', %(search_query)s)) as text_score
        FROM {table_name} e
        JOIN {collection_table} c ON e.collection_id = c.uuid
        WHERE {base_where} AND ({text_clause})
        ORDER BY text_score DESC
        """

        params = {**text_params, 'search_query': req.search_query,
                  'index_name': req.index_name}
        return sql, params

    @staticmethod
    def _build_metadata_only_query_with_join(table_name: str,
                                             collection_table: str,
                                             base_where: str) -> Tuple[str, Dict[str, Any]]:
        """构建仅元数据过滤查询 - 带 JOIN"""
        sql = f"""
        SELECT e.id, e.document, e.cmetadata, e.embedding
        FROM {table_name} e
        JOIN {collection_table} c ON e.collection_id = c.uuid
        WHERE {base_where}
        ORDER BY e.id DESC
        """

        return sql, {}

    @staticmethod
    def _build_metadata_only_query(table_name: str, metadata_where: str) -> Tuple[str, Dict[str, Any]]:
        """构建仅元数据过滤查询"""
        sql = f"""
        SELECT id, document, cmetadata, embedding
        FROM {table_name}
        WHERE {metadata_where}
        ORDER BY id DESC
        """

        return sql, {}
