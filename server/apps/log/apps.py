from django.apps import AppConfig


class LogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.log'

    def ready(self):
        # 初始化默认数据流default
        from apps.log.models import Stream
        if not Stream.objects.filter(id='default').exists():
            Stream.objects.create(id='default', name='Default', created_by="system", updated_by="system")
