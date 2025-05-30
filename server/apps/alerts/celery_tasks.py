# -- coding: utf-8 --
# @File: celery_tasks.py
# @Time: 2025/5/9 14:56
# @Author: windyzhao
from celery import shared_task

from apps.alerts.common.alert_processor import AlertProcessor
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
