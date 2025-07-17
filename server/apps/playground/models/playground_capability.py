from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from django.db import models
import config
from mptt.models import MPTTModel

class PlayGroundCapability(MaintainerInfo, TimeInfo):
    name = models.CharField(max_length=255)
    
    description = models.TextField()
    
    category = models.ForeignKey(
        "PlayGroundCategory",
        on_delete=models.CASCADE,
        related_name="capabilities",
        verbose_name="所属类别",
    )
    
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    
    url= models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="能力链接",
        help_text="能力的访问链接，可选",
    ) 

    config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="配置",
        help_text="能力的配置参数，存储为JSON格式",
    )
    
    class Meta:
        verbose_name = "体验应用能力"
        verbose_name_plural = "体验应用能力"

    def __str__(self):
        return self.name