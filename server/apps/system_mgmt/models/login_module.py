from django.db import models
from django.utils.functional import cached_property

from apps.core.mixinx import EncryptMixin


class LoginModule(models.Model, EncryptMixin):
    name = models.CharField(max_length=100)
    source_type = models.CharField(max_length=50, default="wechat")
    app_id = models.CharField(max_length=100, null=True, blank=True)
    app_secret = models.CharField(max_length=200, null=True, blank=True)
    other_config = models.JSONField(default=dict)
    enabled = models.BooleanField(default=True)
    is_build_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ("name", "source_type")

    def save(self, *args, **kwargs):
        config = {"app_secret": self.app_secret}
        self.decrypt_field("app_secret", config)
        self.encrypt_field("app_secret", config)
        self.app_secret = config["app_secret"]
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_app_secret(self):
        config = {"app_secret": self.app_secret}
        self.decrypt_field("app_secret", config)
        return config["app_secret"]
