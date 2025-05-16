from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    app = models.CharField(max_length=50, null=True, blank=True, default="")
    menu_list = models.JSONField(default=list)

    class Meta:
        unique_together = ("name", "app")
