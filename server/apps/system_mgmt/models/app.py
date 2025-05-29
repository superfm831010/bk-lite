from django.db import models


class App(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    description_cn = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=255)
    is_build_in = models.BooleanField(default=True)
    tags = models.JSONField(default=list)
