from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    disabled = models.BooleanField(default=False)
    locale = models.CharField(max_length=32, default="zh-Hans")
    timezone = models.CharField(max_length=32, default="Asia/Shanghai")
    group_list = models.JSONField(default=list)
    role_list = models.JSONField(default=list)

    @staticmethod
    def display_fields():
        return [
            "id",
            "username",
            "display_name",
            "email",
            "disabled",
            "locale",
            "timezone",
        ]


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    parent_id = models.IntegerField(default=0)

    class Meta:
        unique_together = ("name", "parent_id")
