from django.db import models
from django.utils.functional import cached_property

from apps.core.encoders import PrettyJSONEncoder
from apps.core.mixinx import EncryptMixin


class EmbedModelChoices(models.TextChoices):
    LANG_SERVE = "lang-serve", "LangServe"


class EmbedProvider(models.Model, EncryptMixin):
    name = models.CharField(max_length=255, verbose_name="名称")
    embed_model_type = models.CharField(max_length=255, choices=EmbedModelChoices.choices, verbose_name="嵌入模型")
    embed_config = models.JSONField(
        verbose_name="嵌入配置",
        blank=True,
        null=True,
        encoder=PrettyJSONEncoder,
        default=dict,
    )
    enabled = models.BooleanField(default=True, verbose_name="是否启用")
    team = models.JSONField(default=list)
    is_build_in = models.BooleanField(default=False, verbose_name="是否内置")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Embed模型"
        verbose_name_plural = verbose_name
        db_table = "model_provider_mgmt_embedprovider"

    def save(self, *args, **kwargs):
        if "api_key" in self.embed_config:
            self.decrypt_field("api_key", self.embed_config)
            self.encrypt_field("api_key", self.embed_config)
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_embed_config(self):
        embed_config_decrypted = self.embed_config.copy()

        if "api_key" in embed_config_decrypted:
            self.decrypt_field("api_key", embed_config_decrypted)
        return embed_config_decrypted
