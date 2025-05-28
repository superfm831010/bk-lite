# -- coding: utf-8 --
# @File: celery_tasks.py
# @Time: 2025/5/9 14:56
# @Author: windyzhao
from celery import shared_task

from apps.alerts.common.alert_processor import AlertProcessor
from apps.alerts.models import Alert
from apps.core.logger import logger


@shared_task
def event_aggregation_alert(window_size="10min"):
    """
    每分钟执行的聚合任务
    """
    logger.info("event aggregation alert task start!")
    processor = AlertProcessor(window_size=window_size)
    processor.main()
    logger.info("event aggregation alert task end!")


@shared_task
def update_alert_search_vectors(alert_ids):
    """异步批量更新告警的搜索向量"""
    from django.db import connection

    # 假设搜索向量是基于标题和内容的组合
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE alerts_alert 
            SET search_vector = to_tsvector('jiebacfg', COALESCE(title, '') || ' ' || COALESCE(content, '')) 
            WHERE id IN %s
            """,
            [tuple(alert_ids)]
        )

    return f"Updated search vectors for {len(alert_ids)} alerts"
