from typing import List
from xml.dom.minidom import Document

from pydantic import BaseModel
from src.rag.graph_rag.graphiti.metis_embedder import MetisEmbedder
from src.rag.graph_rag.graphiti.metis_embedder_config import MetisEmbedderConfig
from src.rag.graph_rag.graphiti.metis_raranker_config import MetisRerankerConfig
from src.rag.graph_rag.graphiti.metis_reranker_client import MetisRerankerClient
from src.summarize.summarize_manager import SummarizeManager
from tqdm import tqdm
from graphiti_core import Graphiti
from src.core.env.core_settings import core_settings
from src.entity.rag.base.document_count_request import DocumentCountRequest
from src.entity.rag.base.document_delete_request import DocumentDeleteRequest
from src.entity.rag.base.document_ingest_request import GraphRagDocumentIngestRequest
from graphiti_core.nodes import EpisodeType
from src.entity.rag.base.document_list_request import DocumentListRequest
from src.entity.rag.base.document_metadata_update_request import DocumentMetadataUpdateRequest
from src.entity.rag.base.document_retriever_request import DocumentRetrieverRequest
from src.entity.rag.base.index_delete_request import IndexDeleteRequest
from src.rag.base_rag import BaseRag
from graphiti_core.llm_client import OpenAIClient, LLMConfig
from openai import AsyncOpenAI
from datetime import datetime, timezone


class GraphitiRAG():
    def __init__(self):
        pass

    def update_metadata(self, req: DocumentMetadataUpdateRequest):
        pass

    def count_index_document(self, req: DocumentCountRequest):
        pass

    def delete_index(self, req: IndexDeleteRequest):
        pass

    def list_index_document(self, req: DocumentListRequest):
        pass

    def delete_document(self, req: DocumentDeleteRequest):
        pass

    async def setup_graph(self):
        graphiti = Graphiti(
            core_settings.neo4j_host,
            core_settings.neo4j_username,
            core_settings.neo4j_password,
        )
        await graphiti.build_indices_and_constraints()

    async def ingest(self, req: GraphRagDocumentIngestRequest):
        llm_client = AsyncOpenAI(
            api_key=req.openai_api_key,
            base_url=req.openai_api_base,
        )

        embed_client = MetisEmbedder(
            MetisEmbedderConfig(
                url=req.embed_model_base_url,
                model_name=req.embed_model_name,
                api_key=req.embed_model_api_key
            )
        )

        rerank_client = MetisRerankerClient(
            MetisRerankerConfig(
                url=req.rerank_model_base_url,
                model_name=req.rerank_model_name,
                api_key=req.rerank_model_api_key
            )
        )

        graphiti_instance = Graphiti(
            core_settings.neo4j_host,
            core_settings.neo4j_username,
            core_settings.neo4j_password,
            llm_client=OpenAIClient(
                client=llm_client,
                config=LLMConfig(
                    model=req.openai_model,
                    small_model=req.openai_small_model,
                ),
            ),
            embedder=embed_client,
            cross_encoder=rerank_client
        )

        for doc in tqdm(req.docs):
            source_description = SummarizeManager.summarize(content=doc.page_content,
                                                            model='local:textrank',
                                                            openai_api_base='',
                                                            openai_api_key='')

            await graphiti_instance.add_episode(
                name=doc.metadata['chunk_id'],
                episode_body=doc.page_content,
                source=EpisodeType.text,
                source_description=source_description,
                reference_time=datetime.now(timezone.utc),
            )

    def search(self, req: DocumentRetrieverRequest) -> List[Document]:
        pass

    def process_recall_stage(self, req: DocumentRetrieverRequest, search_result: List[Document]) -> List[Document]:
        pass
