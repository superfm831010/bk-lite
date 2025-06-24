from typing import List
from langchain_core.documents import Document
from src.entity.rag.base.document_delete_request import DocumentDeleteRequest
from src.entity.rag.graphiti.document_ingest_request import GraphitiRagDocumentIngestRequest
from src.entity.rag.graphiti.document_list_request import DocumentListRequest
from src.entity.rag.graphiti.document_retriever_request import DocumentRetrieverRequest
from src.rag.graph_rag.graphiti.metis_embedder import MetisEmbedder
from src.rag.graph_rag.graphiti.metis_embedder_config import MetisEmbedderConfig
from src.rag.graph_rag.graphiti.metis_raranker_config import MetisRerankerConfig
from src.rag.graph_rag.graphiti.metis_reranker_client import MetisRerankerClient
from src.summarize.summarize_manager import SummarizeManager
from tqdm import tqdm
from graphiti_core import Graphiti
from src.core.env.core_settings import core_settings
from graphiti_core.nodes import EpisodeType
from src.entity.rag.base.index_delete_request import IndexDeleteRequest
from graphiti_core.llm_client import OpenAIClient, LLMConfig
from openai import AsyncOpenAI
from datetime import datetime, timezone


class GraphitiRAG():
    def __init__(self):
        pass

    async def delete_index(self, req: IndexDeleteRequest):
        graphiti = Graphiti(
            core_settings.neo4j_host,
            core_settings.neo4j_username,
            core_settings.neo4j_password,
        )
        await graphiti.driver.execute_query(
            f"""
            MATCH (n {{group_id: '{req.group_id}'}})
            DETACH DELETE n
            """
        )

    async def list_index_document(self, req: DocumentListRequest):
        graphiti = Graphiti(
            core_settings.neo4j_host,
            core_settings.neo4j_username,
            core_settings.neo4j_password,
        )
        # First get all nodes
        nodes_result = await graphiti.driver.execute_query(
            f"""
            MATCH (n) WHERE n.group_id = '{req.group_id}'
            RETURN n.name as name, n.uuid as uuid, n.fact as fact, n.summary as summary, id(n) as node_id
            """
        )

        # Then get all relationships
        edges_result = await graphiti.driver.execute_query(
            f"""
            MATCH (n)-[r]-(m) 
            WHERE n.group_id = '{req.group_id}' AND m.group_id = '{req.group_id}'
            RETURN type(r) as relation_type, 
                   n.uuid as source_uuid, 
                   m.uuid as target_uuid,
                   n.name as source_name,
                   m.name as target_name,
                   id(n) as source_id,
                   id(m) as target_id
            """
        )

        # Build edges list
        edges = []
        for edge_record in edges_result.records:
            edge = {
                'relation_type': edge_record['relation_type'],
                'source': edge_record['source_uuid'],
                'target': edge_record['target_uuid'],
                'source_name': edge_record['source_name'],
                'target_name': edge_record['target_name'],
                'source_id': edge_record['source_id'],
                'target_id': edge_record['target_id']
            }
            edges.append(edge)

        docs = []
        for record in nodes_result.records:
            doc = Document(
                page_content=record['fact'] or record['summary'] or '',
                metadata={
                    'name': record['name'],
                    'uuid': record['uuid'],
                    'group_id': req.group_id,
                    'node_id': record['node_id'],
                    'edges': edges
                }
            )
            docs.append(doc)

        return docs

    async def delete_document(self, req: DocumentDeleteRequest):
        graphiti = Graphiti(
            core_settings.neo4j_host,
            core_settings.neo4j_username,
            core_settings.neo4j_password,
        )
        await graphiti.remove_episode(
            episode_uuid=req.uuid,
        )

    async def setup_graph(self):
        graphiti = Graphiti(
            core_settings.neo4j_host,
            core_settings.neo4j_username,
            core_settings.neo4j_password,
        )
        await graphiti.build_indices_and_constraints()

    async def build_communities(self, graphiti_instance: Graphiti, group_ids: List[str]):
        await graphiti_instance.build_communities(group_ids=group_ids)

    async def ingest(self, req: GraphitiRagDocumentIngestRequest):
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
                group_id=req.group_id,
            )

        if req.rebuild_community:
            await self.build_communities(graphiti_instance, [req.group_id])

    async def search(self, req: DocumentRetrieverRequest) -> List[Document]:
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
            embedder=embed_client,
            cross_encoder=rerank_client
        )

        result = await graphiti_instance.search(
            query=req.search_query,
            num_results=req.size,
            group_ids=[req.group_id]
        )

        docs = []
        for r in result:
            doc = Document(
                page_content=r.fact,
                metadata={
                    'uuid': r.uuid,
                    'group_id': req.group_id
                }
            )
            docs.append(doc)
        return docs
