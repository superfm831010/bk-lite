# -- coding: utf-8 --
# @File: tasks.py
# @Time: 2025/5/9 14:56
# @Author: windyzhao
import time

from celery import shared_task

from apps.alerts.common.notify.notify import Notify
from apps.alerts.models import SystemSetting
from apps.alerts.service.alter_operator import BeatUpdateAlertStatu
from apps.alerts.service.notify_service import NotifyResultService
from apps.alerts.service.un_dispatch import UnDispatchService
from apps.core.logger import alert_logger as logger


@shared_task
def event_aggregation_alert(window_size="10min"):
    """
    每分钟执行的聚合任务
    """
    logger.info("event aggregation alert task start!")
    try:
        # 移动导入到函数内部避免循环导入
        from apps.alerts.common.aggregation.alert_processor import AlertProcessor

        processor = AlertProcessor(window_size=window_size)

        # 重新加载数据库规则，确保使用最新规则
        logger.info("开始重新加载数据库规则")
        processor.reload_database_rules()

        # 执行聚合处理
        processor.main()
        logger.info("event aggregation alert task end!")

    except Exception as e:
        logger.error(f"聚合任务执行失败: {str(e)}")
        raise


@shared_task
def beat_close_alert():
    """
    告警关闭兜底机制
    """
    logger.info("== beat close alert task start ==")
    beat_update = BeatUpdateAlertStatu(times=3)  # 3个窗口内
    beat_update.beat_close_alert()
    logger.info("== beat close alert task end ==")


@shared_task
def check_and_send_reminders():
    """
    统一的提醒检查任务 - 每分钟执行一次轮询
    检查所有需要发送提醒的告警并处理
    """
    logger.info("== 开始检查提醒任务 ==")
    try:
        from apps.alerts.service.reminder_service import ReminderService
        result = ReminderService.check_and_process_reminders()
        logger.info(f"== 提醒任务检查完成 == 处理={result.get('processed', 0)}, 成功={result.get('success', 0)}")
        return result
    except Exception as e:
        logger.error(f"提醒任务检查失败: {str(e)}")
        return {"processed": 0, "success": 0, "error": str(e)}


@shared_task
def cleanup_reminder_tasks():
    """
    清理过期的提醒任务记录
    每小时执行一次
    """
    logger.info("== 开始清理提醒任务 ==")
    try:
        from apps.alerts.service.reminder_service import ReminderService
        cleaned_count = ReminderService.cleanup_expired_reminders()
        logger.info(f"== 提醒任务清理完成 == 清理了{cleaned_count}条记录")
        return cleaned_count
    except Exception as e:
        logger.error(f"清理提醒任务失败: {str(e)}")
        return 0


@shared_task
def sync_notify(username_list, channel, title, content, object_id="", notify_action_object="alert"):
    """
    同步通知方法
    :param username_list: 用户名列表
    :param channel: 通知渠道
    :param title: 通知标题
    :param content: 通知内容
    :param object_id: 通知对象ID（可选）
    :param notify_action_object: 通知动作对象，默认为"alert"
    """
    send_time = time.time()
    logger.info(
        "=== 开始执行通知任务 time={} username_list={}, channel={} ===".format(send_time, username_list, channel))
    notify = Notify(username_list=username_list, channel=channel, title=title, content=content)
    result = notify.notify()
    logger.info("=== 通知任务执行完成 send_time={}===".format(send_time))
    if object_id:
        notify_result_obj = NotifyResultService(notify_users=username_list, channel=channel, notify_object=object_id,
                                                notify_action_object=notify_action_object, notify_result=result)
        notify_result_obj.save_notify_result()
    return result


@shared_task
def sync_shield(event_list):
    """
    异步屏蔽事件
    """
    logger.info("== 开始执行屏蔽事件任务 ==")
    try:
        from apps.alerts.common.shield import execute_shield_check_for_events
        result = execute_shield_check_for_events(event_list)
        logger.info(f"== 屏蔽事件任务完成 == 处理了{len(event_list)}条事件")
        return result
    except Exception as e:
        logger.error(f"屏蔽事件任务失败: {str(e)}")
        return {"result": False, "error": str(e)}


@shared_task
def sync_no_dispatch_alert_notice_task():
    """
    周期任务，检查那些未能自动分派的告警，进行系统配置的通知
    """
    logger.info("== 开始执行未分派告警通知任务 ==")
    setting_activate = SystemSetting.objects.filter(key="no_dispatch_alert_notice", is_activate=True).exists()
    if not setting_activate:
        logger.info("== 未分派告警通知功能未启用，任务执行结束 ==")
        return

    params = UnDispatchService.notify_un_dispatched_alert_params_format()
    for notify_people, channel, title, content, alerts in params:
        sync_notify(username_list=notify_people, channel=channel, title=title, content=content)

    logger.info("== 未分派告警通知任务执行完成 ==")
