from django.apps import AppConfig
from django.db.models.signals import post_migrate
from apps.core.logger import cmdb_logger as logger


class CmdbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cmdb"

    def ready(self):
        try:
            from apps.cmdb.services.init_migrate import init_network_oid

            post_migrate.connect(init_network_oid, sender=self)
        except Exception as e:
            logger.exception(getattr(e, "message", e))

        import apps.cmdb.nats  # noqa

