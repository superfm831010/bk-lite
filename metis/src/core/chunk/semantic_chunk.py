from typing import List

from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

from .base_chunk import BaseChunk


class SemanticChunk(BaseChunk):
    """语义分块器，基于语义相似度进行文档分割"""
    
    def __init__(self, semantic_embedding_model: OpenAIEmbeddings):
        """
        初始化语义分块器
        
        Args:
            semantic_embedding_model: 用于计算语义相似度的嵌入模型
        """
        self.semantic_embedding_model = semantic_embedding_model
        self.semantic_chunker = SemanticChunker(
            embeddings=semantic_embedding_model,
            sentence_split_regex=r'(?<=[.?!。？！])\s*'
        )

    def _split_documents(self, docs: List[Document]) -> List[Document]:
        """使用语义分块器分割文档"""
        return self.semantic_chunker.split_documents(docs)
