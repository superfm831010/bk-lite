from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .base_chunk import BaseChunk


class RecursiveChunk(BaseChunk):
    """递归字符文本分割器，支持多种分隔符的智能分割"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 128):
        """
        初始化递归分块器
        
        Args:
            chunk_size: 每个块的目标大小
            chunk_overlap: 块之间的重叠大小
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def _split_documents(self, docs: List[Document]) -> List[Document]:
        """使用递归字符分割器分割文档"""
        return self.text_splitter.split_documents(docs)
