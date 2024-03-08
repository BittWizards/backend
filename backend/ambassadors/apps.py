# flake8: noqa
from django.apps import AppConfig


class AmbassadorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ambassadors"

    def ready(self) -> None:
        import ambassadors.signals
