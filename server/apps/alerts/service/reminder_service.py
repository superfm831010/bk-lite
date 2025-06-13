# -- coding: utf-8 --
# @File: reminder_service.py
# @Time: 2025/6/11 10:00
# @Author: windyzhao
import json

from django.db.models import F
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from typing import Dict, Any, Optional

from apps.alerts.constants import LevelType
from apps.alerts.models import Alert, AlertReminderTask, AlertAssignment, Level
from apps.alerts.tasks import sync_notify
from apps.core.logger import logger


class ReminderService:
    """告警提醒服务"""

    @classmethod
    def create_reminder_task(cls, alert: Alert, assignment: AlertAssignment) -> Optional[AlertReminderTask]:
        """创建提醒任务"""
        try:
            # 获取该告警级别的通知频率配置
            alert_level = alert.level
            level_config = assignment.notification_frequency.get(alert_level, {})

            if not level_config or level_config.get('interval_minutes', 0) <= 0:
                logger.warning(f"告警级别 {alert_level} 没有配置通知频率或频率为0，不创建提醒任务")
                return None

            interval_minutes = level_config.get('interval_minutes', 30)
            max_count = level_config.get('max_count', 10)

            # 检查是否已存在活跃的提醒任务
            existing_task = AlertReminderTask.objects.filter(
                alert=alert,
                assignment=assignment,
                is_active=True
            ).first()

            if existing_task:
                logger.warning(f"告警 {alert.alert_id} 已存在活跃的提醒任务")
                return existing_task

            # 创建新的提醒任务
            reminder_task = AlertReminderTask.objects.create(
                alert=alert,
                assignment=assignment,
                is_active=True,
                current_frequency_minutes=interval_minutes,
                current_max_reminders=max_count,
                reminder_count=0,
                next_reminder_time=timezone.now() + timedelta(minutes=interval_minutes),
            )

            logger.info(f"为告警 {alert.alert_id} 创建提醒任务，频率: {interval_minutes}分钟，最大次数: {max_count}")
            return reminder_task

        except Exception as e:
            logger.error(f"创建提醒任务失败: alert_id={alert.alert_id}, error={str(e)}")
            return None

    @classmethod
    def stop_reminder_task(cls, alert: Alert) -> bool:
        """停止告警的提醒任务"""
        try:
            with transaction.atomic():
                updated_count = AlertReminderTask.objects.filter(
                    alert=alert,
                    is_active=True
                ).update(
                    is_active=False,
                    completed_at=timezone.now()
                )

                if updated_count > 0:
                    logger.info(f"停止告警 {alert.alert_id} 的 {updated_count} 个提醒任务")
                    return True
                else:
                    logger.warning(f"告警 {alert.alert_id} 没有找到活跃的提醒任务")
                    return False

        except Exception as e:
            logger.error(f"停止提醒任务失败: alert_id={alert.alert_id}, error={str(e)}")
            return False

    @classmethod
    def _update_reminder_task(cls, reminder: AlertReminderTask, new_frequency: int, new_max_count: int) -> bool:
        """更新提醒任务配置"""
        try:
            with transaction.atomic():
                old_frequency = reminder.current_frequency_minutes
                old_max_count = reminder.current_max_reminders

                reminder.current_frequency_minutes = new_frequency
                reminder.current_max_reminders = new_max_count

                # 如果频率发生变化，需要重新计算下次提醒时间
                if old_frequency != new_frequency:
                    now = timezone.now()
                    # 如果下次提醒时间还没到，按新频率重新计算
                    if reminder.next_reminder_time > now:
                        time_since_last = now - reminder.last_reminder_time if reminder.last_reminder_time else timedelta(0)
                        remaining_time = timedelta(minutes=new_frequency) - time_since_last
                        if remaining_time.total_seconds() > 0:
                            reminder.next_reminder_time = now + remaining_time
                        else:
                            reminder.next_reminder_time = now

                reminder.save()

                logger.info(f"更新提醒任务配置: alert_id={reminder.alert.alert_id}, "
                            f"频率: {old_frequency}->{new_frequency}分钟, "
                            f"最大次数: {old_max_count}->{new_max_count}")
                return True

        except Exception as e:
            logger.error(f"更新提醒任务配置失败: reminder_id={reminder.id}, error={str(e)}")
            return False

    @classmethod
    def check_and_process_reminders(cls) -> Dict[str, Any]:
        """检查并处理需要发送的提醒"""
        processed = 0
        success = 0
        now = timezone.now()

        try:
            # 获取需要发送提醒的任务
            pending_reminders = AlertReminderTask.objects.filter(
                is_active=True,
                next_reminder_time__lte=now,
                reminder_count__lt=F('current_max_reminders')
            ).select_related('alert', 'assignment')

            for reminder in pending_reminders:
                processed += 1

                try:
                    # 发送提醒通知
                    if cls._send_reminder_notification(reminder):
                        # 更新提醒记录
                        reminder.reminder_count += 1
                        reminder.last_reminder_time = now

                        # 计算下次提醒时间
                        if reminder.reminder_count < reminder.current_max_reminders:
                            reminder.next_reminder_time = now + timedelta(minutes=reminder.current_frequency_minutes)
                        else:
                            # 达到最大次数，停止提醒
                            reminder.is_active = False

                        reminder.save()
                        success += 1

                except Exception as e:
                    logger.error(f"处理提醒任务失败: reminder_id={reminder.alert.alert_id}, error={str(e)}")

        except Exception as e:
            logger.error(f"检查提醒任务失败: {str(e)}")

        return {
            "processed": processed,
            "success": success
        }

    @classmethod
    def _send_reminder_notification(cls, reminder: AlertReminderTask) -> bool:
        """发送提醒通知"""
        try:
            username_list = reminder.assignment.personnel
            if not username_list:
                logger.warning(f"提醒任务 {reminder.id} 没有配置接收人员，无法发送通知")
                return False

            channel_list = reminder.assignment.notify_channels
            if isinstance(channel_list, str):
                try:
                    channel_list = json.loads(channel_list)
                except json.JSONDecodeError:
                    logger.error(f"提醒任务 {reminder.id} 的通知渠道配置错误: {channel_list}")
                    channel_list = []

            if not channel_list:
                logger.warning(f"提醒任务 {reminder.id} 没有配置通知渠道，无法发送通知")
                return False

            title = cls.format_title(reminder.alert)
            content = cls.format_content(reminder.alert)
            for channel in channel_list:
                sync_notify.delay(username_list, channel, title, content)

        except Exception as e:
            logger.error(f"发送提醒通知失败: reminder_id={reminder.id}, error={str(e)}")
            return False

    @staticmethod
    def format_title(alert: Alert) -> str:
        """格式化提醒标题"""
        title = alert.title
        return title

    @classmethod
    def format_content(cls, alert: Alert) -> str:
        """格式化提醒内容"""
        alert_level_map = cls.search_level_map(level_type=LevelType.ALERT)
        content = f"告警对象: {alert.resource_type}\n"
        content += f"告警级别: {alert_level_map[alert.level]}\n"
        content += f"告警指标: {alert.item}\n"
        content += f"告警内容: {alert.content}\n"
        content += f"告警时间: {alert.format_created_at}\n"
        return content

    @staticmethod
    def search_level_map(level_type) -> Dict[str, str]:
        instance = Level.objects.filter(level_type=level_type).values_list("level_id", "level_display_name")
        return {str(i[0]): i[1] for i in instance}

    @classmethod
    def cleanup_expired_reminders(cls) -> int:
        """清理过期的提醒任务记录"""
        try:
            # 清理30天前完成的提醒任务
            cutoff_time = timezone.now() - timedelta(days=30)

            deleted_count = AlertReminderTask.objects.filter(
                is_active=False,
                updated_at__lt=cutoff_time
            ).delete()[0]

            logger.info(f"清理了 {deleted_count} 条过期的提醒任务记录")
            return deleted_count

        except Exception as e:
            logger.error(f"清理过期提醒任务失败: {str(e)}")
            return 0
