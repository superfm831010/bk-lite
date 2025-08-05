from django.db import models
from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.playground.models.playground_capability import PlayGroundCapability

class PlayGroundFile(MaintainerInfo, TimeInfo):
    capability = models.ForeignKey(
        PlayGroundCapability,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="能力演示ID"
    )
    name = models.CharField(max_length=255, verbose_name="文件名称")
    train_data = models.JSONField(
        verbose_name="文件数据",
        help_text="训练数据，包含timestamp和value"
    )
    is_active = models.BooleanField(default=True, verbose_name="是否启用")

    class Meta:
        verbose_name = "能力演示文件"
        verbose_name_plural = "能力演示文件"

    def __str__(self):
        return self.name