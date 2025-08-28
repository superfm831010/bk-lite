from django.db import models
from django.utils.functional import cached_property

from apps.core.encoders import PrettyJSONEncoder
from apps.core.mixinx import EncryptMixin


class LLMModel(models.Model, EncryptMixin):
    name = models.CharField(max_length=255, verbose_name="名称")
    llm_config = models.JSONField(
        verbose_name="LLM配置",
        blank=True,
        null=True,
        encoder=PrettyJSONEncoder,
        default=dict,
    )
    enabled = models.BooleanField(default=True, verbose_name="启用")
    team = models.JSONField(default=list)
    is_build_in = models.BooleanField(default=True, verbose_name="是否内置")
    is_demo = models.BooleanField(default=False)
    consumer_team = models.CharField(default="", blank=True, null=True, max_length=64)
    model_type = models.ForeignKey("ModelType", on_delete=models.SET_NULL, verbose_name="模型类型", blank=True, null=True)
    label = models.CharField(max_length=100, verbose_name="标签", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if "openai_api_key" in self.llm_config:
            self.decrypt_field("openai_api_key", self.llm_config)
            self.encrypt_field("openai_api_key", self.llm_config)
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_llm_config(self):
        llm_config_decrypted = self.llm_config.copy()

        if "openai_api_key" in llm_config_decrypted:
            self.decrypt_field("openai_api_key", llm_config_decrypted)
        return llm_config_decrypted

    class Meta:
        verbose_name = "LLM模型"
        verbose_name_plural = verbose_name
        db_table = "model_provider_mgmt_llmmodel"


class ModelType(models.Model):
    name = models.CharField(max_length=50, verbose_name="模型类型名称", unique=True)
    display_name = models.CharField(max_length=100, verbose_name="显示名称")
    icon = models.CharField(max_length=100, verbose_name="图标", blank=True, null=True)
    is_build_in = models.BooleanField(default=False)
    index = models.IntegerField(default=0, verbose_name="排序")
    tags = models.JSONField(default=list)
