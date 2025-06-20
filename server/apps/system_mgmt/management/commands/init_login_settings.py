import os

from django.core.management import BaseCommand

from apps.core.logger import system_logger as logger
from apps.system_mgmt.models import Role, SystemSettings
from apps.system_mgmt.models.login_module import LoginModule


class Command(BaseCommand):
    help = "初始登陆化设置"

    def handle(self, *args, **options):
        LoginModule.objects.get_or_create(
            is_build_in=True,
            source_type="wechat",
            defaults={
                "name": "微信开放平台",
                "app_id": "",
                "app_secret": "",
                "other_config": {
                    "redirect_uri": "",
                    "callback_url": "",
                },
                "enabled": True,
            },
        )

        SystemSettings.objects.get_or_create(key="login_expired_time", defaults={"value": "24"})
        SystemSettings.objects.get_or_create(key="enable_otp", defaults={"value": "0"})
        init_canway_login_module()


def init_canway_login_module():
    erp_namespace = os.getenv("ERP_NAMESPACE", "")
    if not erp_namespace:
        logger.info("ERP_NAMESPACE环境变量未设置，跳过嘉为科技登录模块初始化")
        return

    role = Role.objects.get(app="opspilot", name="normal")
    login_module, created = LoginModule.objects.get_or_create(
        name="嘉为科技",
        source_type="bk_lite",
        is_build_in=True,
        defaults={
            "other_config": {
                "namespace": erp_namespace,
                "root_group": "嘉为科技",
                "domain": "canway.net",
                "default_roles": [role.id],
                "sync": True,
                "sync_time": "00:00",
            },
            "enabled": True,
        },
    )

    if login_module.other_config.get("sync", False):
        login_module.create_sync_periodic_task(login_module)
