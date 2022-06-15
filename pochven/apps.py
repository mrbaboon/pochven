from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PochvenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pochven'

    def ready(self):
        import pochven.management.post_migrate as pm_handlers

        post_migrate.connect(pm_handlers.register_permissions)
