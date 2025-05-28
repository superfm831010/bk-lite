# -- coding: utf-8 --
# @File: config.py
# @Time: 2025/5/9 14:56
# @Author: windyzhao


from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'event_aggregation_alert': {
        'task': 'apps.alerts.celery_tasks.event_aggregation_alert',
        'schedule': crontab(minute='*'),  # 每分钟执行
    },
}
