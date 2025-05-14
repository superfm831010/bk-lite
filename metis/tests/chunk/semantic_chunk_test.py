import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from src.chunk.semantic_chunk import SemanticChunk
from src.embed.embed_builder import EmbedBuilder
from src.loader.text_loader import TextLoader


def test_semantic_chunk():
    embeddings = EmbedBuilder.get_embed(
        "local:huggingface_embedding:BAAI/bge-small-zh-v1.5")

    chunk = SemanticChunk(embeddings)
    loader = TextLoader(
        path='./tests/assert/full_text_loader.txt', load_mode='full')
    docs = loader.load()
    rs = chunk.chunk(docs)
    print(rs)
