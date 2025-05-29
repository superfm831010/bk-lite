# -- coding: utf-8 --
# @File: update_search_vectors.py
# @Time: 2025/5/29 10:47
# @Author: windyzhao

from django.core.management.base import BaseCommand
from apps.alerts.models import Alert, Event


class Command(BaseCommand):
    help = '更新告警和事件的全文搜索向量'

    def handle(self, *args, **options):
        # 更新所有告警的搜索向量
        alerts = Alert.objects.filter(search_vector__isnull=True)
        for alert in alerts:
            alert.update_search_vector()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {alerts.count()} alert search vectors')
        )

        # 更新所有事件的搜索向量
        events = Event.objects.filter(search_vector__isnull=True)
        for event in events:
            event.update_search_vector()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {events.count()} event search vectors')
        )
