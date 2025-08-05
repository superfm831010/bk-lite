from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class KnowledgeGraph(MaintainerInfo, TimeInfo):
    knowledge_base = models.OneToOneField("KnowledgeBase", on_delete=models.CASCADE)
    llm_model = models.ForeignKey("LLMModel", on_delete=models.CASCADE)
    rerank_model = models.ForeignKey("RerankProvider", on_delete=models.CASCADE, null=True, blank=True)
    embed_model = models.ForeignKey("EmbedProvider", on_delete=models.CASCADE, null=True, blank=True)
    rebuild_community = models.BooleanField(default=False, verbose_name="是否重建社区")
    doc_list = models.JSONField(default=list)
    status = models.CharField(max_length=50, default="completed", verbose_name="状态")


class GraphChunkMap(models.Model):
    knowledge_graph = models.ForeignKey(KnowledgeGraph, on_delete=models.CASCADE)
    chunk_id = models.CharField(max_length=255, verbose_name="Chunk ID")
    graph_id = models.CharField(max_length=255, verbose_name="Graph ID")
