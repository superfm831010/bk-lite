"""
PostgreSQL + pgvector RAG 配置
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PgvectorConfig:
    """PostgreSQL + pgvector 配置类"""

    # 批处理配置
    batch_size: int = 100  # 批量插入的文档数量
    max_retries: int = 3   # 最大重试次数
    retry_delay: float = 1.0  # 重试延迟（秒）

    # 连接池配置
    connection_pool_size: int = 10  # 连接池大小
    connection_pool_max_overflow: int = 20  # 连接池最大溢出
    connection_timeout: int = 30  # 连接超时（秒）

    # 性能优化配置
    enable_parallel_embedding: bool = True  # 是否启用并行嵌入计算
    embedding_batch_size: int = 50  # 嵌入计算批次大小

    # 索引配置
    enable_hnsw_index: bool = True  # 是否启用HNSW索引
    hnsw_m: int = 16  # HNSW索引参数m
    hnsw_ef_construction: int = 200  # HNSW索引构建参数

    # 内存优化配置
    max_memory_usage_mb: int = 1024  # 最大内存使用量（MB）
    enable_memory_mapping: bool = False  # 是否启用内存映射

    @classmethod
    def get_default_config(cls) -> 'PgvectorConfig':
        """获取默认配置"""
        return cls()

    @classmethod
    def get_performance_config(cls) -> 'PgvectorConfig':
        """获取性能优化配置"""
        return cls(
            batch_size=200,
            enable_parallel_embedding=True,
            embedding_batch_size=100,
            enable_hnsw_index=True,
            hnsw_m=32,
            hnsw_ef_construction=400,
            max_memory_usage_mb=2048
        )

    @classmethod
    def get_memory_efficient_config(cls) -> 'PgvectorConfig':
        """获取内存优化配置"""
        return cls(
            batch_size=50,
            enable_parallel_embedding=False,
            embedding_batch_size=25,
            max_memory_usage_mb=512,
            enable_memory_mapping=True
        )

    def validate(self) -> bool:
        """验证配置的有效性"""
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.embedding_batch_size <= 0:
            raise ValueError("embedding_batch_size must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")
        if self.max_memory_usage_mb <= 0:
            raise ValueError("max_memory_usage_mb must be positive")

        return True
