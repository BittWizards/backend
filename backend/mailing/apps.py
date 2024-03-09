# flake8: noqa
from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"

    def ready(self) -> None:
        import mailing.signals
