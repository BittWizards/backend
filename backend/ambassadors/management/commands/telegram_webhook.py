import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from rest_framework import status


class Command(BaseCommand):
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--set",
            default=False,
            action="store_true",
            help="Установить webhook для бота",
        )
        parser.add_argument(
            "-p", "--path", help="Указать определенный endpoint для webhook"
        )
        parser.add_argument(
            "-r",
            "--remove",
            default=False,
            action="store_true",
            help="Убрать webhook для бота",
        )

    def handle(self, *args, **kwargs):
        if kwargs["set"]:
            if kwargs["path"]:
                response = requests.post(
                    self.url
                    + (
                        f"SetWebhook?url=https://{settings.DOMAIN}/"
                        f"{kwargs['path']}"
                    )
                )
                if response.status_code == status.HTTP_200_OK:
                    print(
                        "Webhook настроен на адрес "
                        f"https://{settings.DOMAIN}/{kwargs['path']}"
                    )
                else:
                    print(
                        "Не удалость подключить webhook, проверьто что домен "
                        "указан правильно и у вас имеются для него сертификаты."
                    )
            else:
                response = requests.post(
                    self.url
                    + f"SetWebhook?url=https://{settings.DOMAIN}/api/tg"
                )
                if response.status_code == status.HTTP_200_OK:
                    print(
                        "Webhook настроен на адрес "
                        f"https://{settings.DOMAIN}/api/tg"
                    )
                else:
                    print(
                        "Не удалость подключить webhook, проверьто что домен "
                        "указан правильно и у вас имеются для него сертификаты."
                    )
        elif kwargs["remove"]:
            response = requests.post(self.url + "DeleteWebhook")
            if response.status_code == status.HTTP_200_OK:
                print("Webhook успешно удален.")
            else:
                print("Что-то полшло не так.")
        elif kwargs["path"]:
            response = requests.post(
                self.url + f"SetWebhook?url={kwargs['path']}"
            )
            if response.status_code == status.HTTP_200_OK:
                print(
                    "Webhook настроен на адрес "
                    f"https://{settings.DOMAIN}/{kwargs['path']}"
                )
            else:
                print(
                    "Не удалость подключить webhook, проверьто что домен "
                    "указан правильно и у вас имеются для него сертификаты."
                )
