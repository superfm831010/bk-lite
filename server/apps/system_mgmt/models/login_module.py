from django.db import models
from django.utils.functional import cached_property

from apps.core.logger import system_logger as logger
from apps.core.mixinx import EncryptMixin


class LoginModule(models.Model, EncryptMixin):
    name = models.CharField(max_length=100)
    source_type = models.CharField(max_length=50, default="wechat")
    app_id = models.CharField(max_length=100, null=True, blank=True)
    app_secret = models.CharField(max_length=200, null=True, blank=True)
    other_config = models.JSONField(default=dict)
    enabled = models.BooleanField(default=True)
    is_build_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ("name", "source_type")

    def save(self, *args, **kwargs):
        config = {"app_secret": self.app_secret}
        self.decrypt_field("app_secret", config)
        self.encrypt_field("app_secret", config)
        self.app_secret = config["app_secret"]
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_app_secret(self):
        config = {"app_secret": self.app_secret}
        self.decrypt_field("app_secret", config)
        return config["app_secret"]

    def create_sync_periodic_task(self):
        from django.utils import timezone
        from django_celery_beat.models import CrontabSchedule, PeriodicTask

        """创建用户同步周期任务"""
        sync_time = self.other_config.get("sync_time", "00:00")
        hour, minute = map(int, sync_time.split(":"))

        # 创建或获取crontab调度
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone=timezone.get_current_timezone(),
        )

        # 创建周期任务
        task_name = f"sync_user_group_{self.name}"
        PeriodicTask.objects.get_or_create(
            name=task_name,
            defaults={
                "crontab": schedule,
                "task": "apps.system_mgmt.tasks.sync_user_and_group_by_login_module",
                "args": f"[{self.id}]",
                "enabled": True,
            },
        )
        logger.info(f"已创建用户同步周期任务: {task_name}, 执行时间: {sync_time}")
