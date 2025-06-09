# -- coding: utf-8 --
# @File: tasks.py
# @Time: 2025/5/9 14:56
# @Author: windyzhao
from celery import shared_task

from apps.alerts.common.alert_processor import AlertProcessor
from apps.alerts.service.alter_operator import BeatUpdateAlertStatu
from apps.core.logger import logger


@shared_task
def event_aggregation_alert(window_size="10min"):
    """
    每分钟执行的聚合任务
    """
    print("== event aggregation alert task start ==")
    logger.info("event aggregation alert task start!")
    processor = AlertProcessor(window_size=window_size)
    processor.main()
    print("event aggregation alert task end!")
    logger.info("event aggregation alert task end!")


@shared_task
def beat_close_alert():
    """
    告警关闭兜底机制
    """
    logger.info("== beat close alert task start ==")
    beat_update = BeatUpdateAlertStatu(times=10)  # 10个窗口内
    beat_update.beat_close_alert()
    logger.info("== beat close alert task end ==")
