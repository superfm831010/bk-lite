import logging

from django.core.management import BaseCommand

from apps.system_mgmt.models import SystemSettings
from apps.system_mgmt.models.login_module import LoginModule

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "初始登陆化设置"

    def handle(self, *args, **options):
        LoginModule.objects.get_or_create(
            name="Wechat Open Platform",
            source_type="wechat",
            defaults={
                "app_id": "",
                "app_secret": "",
                "other_config": {
                    "redirect_uri": "",
                    "callback_url": "",
                },
                "enabled": True,
                "is_build_in": True,
            },
        )

        SystemSettings.objects.get_or_create(key="login_expired_time", defaults={"value": "24"})
        SystemSettings.objects.get_or_create(key="enable_otp", defaults={"value": "0"})
