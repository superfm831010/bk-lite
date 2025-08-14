from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .base_chunk import BaseChunk


class FixedSizeChunk(BaseChunk):
    """固定大小分块器，不设置重叠"""
    
    def __init__(self, chunk_size: int = 500):
        """
        初始化固定大小分块器
        
        Args:
            chunk_size: 每个块的固定大小
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False,
        )

    def _split_documents(self, docs: List[Document]) -> List[Document]:
        """使用固定大小分割器分割文档"""
        return self.text_splitter.split_documents(docs)
