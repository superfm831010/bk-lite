# -- coding: utf-8 --
# @File: receiver.py
# @Time: 2025/5/13 14:15
# @Author: windyzhao
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.alerts.models import Event


# 通过信号自动更新 search_vector
@receiver(post_save, sender=Event)
def update_event_search_vector(sender, instance, **kwargs):
    instance.update_search_vector()
