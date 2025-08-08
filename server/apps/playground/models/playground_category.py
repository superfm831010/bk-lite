from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from django.db import models
from mptt.models import MPTTModel

class PlayGroundCategory(MaintainerInfo, TimeInfo, MPTTModel):
    name = models.CharField(max_length=255, verbose_name="类别名称", unique=True)
    description = models.TextField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
        verbose_name="父分类",
    )
    
    class Meta:
        verbose_name = "体验应用类别"
        verbose_name_plural = "体验应用类别"
    
    def __str__(self):
        return self.name