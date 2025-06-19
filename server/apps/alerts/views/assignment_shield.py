# -- coding: utf-8 --
# @File: assignment_shield.py
# @Time: 2025/6/10 15:58
# @Author: windyzhao
from apps.alerts.filters import AlertAssignmentModelFilter, AlertShieldModelFilter
from apps.alerts.serializers.serializers import AlertAssignmentModelSerializer, AlertShieldModelSerializer
from config.drf.pagination import CustomPageNumberPagination
from config.drf.viewsets import ModelViewSet
from apps.alerts.models import AlertAssignment, AlertReminderTask, AlertShield
from apps.core.logger import alert_logger as logger


class AlertAssignmentModelViewSet(ModelViewSet):
    """
    告警分派策略视图集
    """
    queryset = AlertAssignment.objects.all()
    serializer_class = AlertAssignmentModelSerializer
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    filterset_class = AlertAssignmentModelFilter
    pagination_class = CustomPageNumberPagination

    def perform_update(self, serializer):
        """更新分派策略时，同步更新相关的提醒任务配置"""
        old_instance = self.get_object()
        old_notification_frequency = old_instance.notification_frequency

        # 保存更新
        updated_instance = serializer.save()
        new_notification_frequency = updated_instance.notification_frequency

        # 检查通知频率配置是否发生变化
        if old_notification_frequency != new_notification_frequency:
            self._update_related_reminders(updated_instance)

    def _update_related_reminders(self, assignment: AlertAssignment):
        """更新相关的提醒任务配置"""
        try:
            # 在方法内部导入以避免循环导入
            from apps.alerts.service.reminder_service import ReminderService

            # 获取所有关联的活跃提醒任务
            active_reminders = AlertReminderTask.objects.filter(
                assignment=assignment,
                is_active=True
            ).select_related('alert')

            for reminder in active_reminders:
                alert_level = reminder.alert.level
                level_config = assignment.notification_frequency.get(alert_level, {})

                # 检查该级别是否还有配置，或配置的频率是否为0
                if not level_config or level_config.get('interval_minutes', 0) <= 0:
                    # 停止该级别的提醒任务
                    ReminderService.stop_reminder_task(reminder.alert)
                    logger.info(f"停止级别为 {alert_level} 的告警 {reminder.alert.alert_id} 的提醒任务")
                else:
                    # 更新提醒配置
                    new_frequency = level_config.get('interval_minutes', 0)
                    new_max_count = level_config.get('max_count', 10)
                    ReminderService._update_reminder_task(reminder, new_frequency, new_max_count)
                    logger.info(
                        f"更新级别为 {alert_level} 的告警 {reminder.alert.alert_id} 的提醒配置: 频率={new_frequency}分钟, 最大次数={new_max_count}")

            logger.info(f"分派策略 {assignment.name} 相关提醒任务配置更新完成")

        except Exception as e:
            logger.error(f"更新提醒任务配置失败: assignment_id={assignment.id}, error={str(e)}")
            raise


class AlertShieldModelViewSet(ModelViewSet):
    """
    告警分派策略视图集
    """
    queryset = AlertShield.objects.all()
    serializer_class = AlertShieldModelSerializer
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    filterset_class = AlertShieldModelFilter
    pagination_class = CustomPageNumberPagination
