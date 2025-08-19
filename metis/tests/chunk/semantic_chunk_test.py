from src.core.chunk.semantic_chunk import SemanticChunk
from src.core.embed import EmbedBuilder
from src.core.loader import TextLoader


def test_semantic_chunk():
    embeddings = EmbedBuilder.get_embed(
        "local:huggingface_embedding:BAAI/bge-small-zh-v1.5")

    chunk = SemanticChunk(embeddings)
    loader = TextLoader(
        path='./tests/assert/full_text_loader.txt', load_mode='full')
    docs = loader.load()
    rs = chunk.chunk(docs)
    print(rs)
