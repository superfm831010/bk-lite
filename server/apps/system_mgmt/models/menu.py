from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    icon = models.CharField(max_length=100, null=True, blank=True)
    order = models.IntegerField(default=0)
    app = models.CharField(max_length=50, default="")
    menu_type = models.CharField(max_length=100, default="")

    class Meta:
        unique_together = ("name", "app")
