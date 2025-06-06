# -- coding: utf-8 --
# @File: config.py
# @Time: 2025/5/9 14:56
# @Author: windyzhao
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'event_aggregation_alert': {
        'task': 'apps.alerts.tasks.event_aggregation_alert',
        'schedule': crontab(minute='*'),  # 每分钟执行
    },
    'beat_close_alert': {
        'task': 'apps.alerts.tasks.beat_close_alert',
        'schedule': crontab(minute='*/5'),  # 每5分钟执行
    },
}
