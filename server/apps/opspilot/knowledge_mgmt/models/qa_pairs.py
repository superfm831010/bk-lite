from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class QAPairs(MaintainerInfo, TimeInfo):
    """问答对模型"""

    # 基础字段
    name = models.CharField(max_length=255, verbose_name="问答对名称")
    description = models.TextField(blank=True, null=True, verbose_name="描述")

    # 外键关系
    knowledge_base = models.ForeignKey("KnowledgeBase", on_delete=models.CASCADE)
    llm_model = models.ForeignKey("LLMModel", on_delete=models.CASCADE)

    # 问答对相关字段
    qa_count = models.IntegerField(default=0, verbose_name="问答对数量")
    document_list = models.JSONField(
        default=list,
        verbose_name="选择的文档列表",
    )
