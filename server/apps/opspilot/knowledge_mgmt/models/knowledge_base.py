from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class KnowledgeBase(MaintainerInfo, TimeInfo):
    name = models.CharField(max_length=100, db_index=True)
    introduction = models.TextField(blank=True, null=True)
    team = models.JSONField(default=list)
    embed_model = models.ForeignKey(
        "EmbedProvider",
        on_delete=models.CASCADE,
        verbose_name=_("Embed Model"),
        blank=True,
        null=True,
    )
    enable_rerank = models.BooleanField(default=True, verbose_name=_("Enable Rerank"))
    rerank_top_k = models.IntegerField(default=10, verbose_name=_("Rerank Top K"))
    rerank_model = models.ForeignKey(
        "RerankProvider",
        on_delete=models.CASCADE,
        verbose_name=_("Rerank Model"),
        blank=True,
        null=True,
    )
    search_type = models.CharField(default="similarity_score_threshold", verbose_name=_("Search Type"), max_length=50)
    score_threshold = models.FloatField(default=0.7, verbose_name=_("Score threshold"))
    enable_naive_rag = models.BooleanField(default=True)
    enable_qa_rag = models.BooleanField(default=True)
    enable_graph_rag = models.BooleanField(default=False)

    rag_recall_mode = models.CharField(default="chunk", max_length=20)

    rag_size = models.IntegerField(default=50)
    qa_size = models.IntegerField(default=50, verbose_name=_("QA size"))
    graph_size = models.IntegerField(default=50, verbose_name=_("Graph size"))

    class Meta:
        db_table = "knowledge_mgmt_knowledgebase"

    def knowledge_index_name(self):
        return f"knowledge_base_{self.id}"

    def delete(self, *args, **kwargs):
        from apps.opspilot.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService

        KnowledgeSearchService.delete_es_index(self.knowledge_index_name())
        super().delete(*args, **kwargs)
