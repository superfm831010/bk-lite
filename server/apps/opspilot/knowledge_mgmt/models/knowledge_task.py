from django.db import models


class KnowledgeTask(models.Model):
    task_name = models.CharField(max_length=100, verbose_name="Task Name")
    train_progress = models.FloatField(default=0, verbose_name="Train Progress")
    knowledge_ids = models.JSONField(default=list, verbose_name="Knowledge IDs")
    knowledge_base_id = models.IntegerField(default=0, verbose_name="Knowledge IDs")
    created_by = models.CharField(max_length=100, verbose_name="Created By")
    domain = models.CharField(max_length=100, default="domain.com", verbose_name="Domain")
    is_qa_task = models.BooleanField(default=False, verbose_name="Is QA Task")
