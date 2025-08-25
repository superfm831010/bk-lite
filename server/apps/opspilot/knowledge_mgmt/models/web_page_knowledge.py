from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.mixinx import PeriodicTaskUtils


class WebPageKnowledge(models.Model, PeriodicTaskUtils):
    url = models.URLField(verbose_name=_("URL"))
    knowledge_document = models.ForeignKey(
        "KnowledgeDocument",
        verbose_name=_("Knowledge Document"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    max_depth = models.IntegerField(verbose_name=_("max depth"), default=1)
    sync_enabled = models.BooleanField(verbose_name=_("Sync Enabled"), default=False)
    sync_time = models.CharField(verbose_name=_("Sync Time"), null=True, blank=True)

    class Meta:
        verbose_name = _("Web Page Knowledge")
        verbose_name_plural = verbose_name
        db_table = "knowledge_mgmt_webpageknowledge"

    def to_dict(self):
        return {
            "url": self.url,
            "max_depth": self.max_depth,
            "sync_enabled": self.sync_enabled,
            "sync_time": self.sync_time,
        }

    def create_sync_periodic_task(self):
        sync_time = self.sync_time or "00:00"
        task_name = f"sync_web_page_knowledge_{self.id}"
        task_args = f"[{self.id}]"
        task_path = "apps.opspilot.tasks.sync_web_page_knowledge"
        self.create_periodic_task(sync_time, task_name, task_args, task_path)

    def delete_sync_periodic_task(self):
        task_name = f"sync_web_page_knowledge_{self.id}"
        self.delete_periodic_task(task_name)
