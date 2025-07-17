from django.apps import AppConfig
from django.db.models.signals import post_migrate


def init_stream(**kwargs):
    # 初始化默认数据流default
    from apps.log.models import Stream
    if not Stream.objects.filter(id='default').exists():
        Stream.objects.create(id='default', name='Default', created_by="system", updated_by="system")


class LogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.log'

    def ready(self):
        post_migrate.connect(init_stream)
