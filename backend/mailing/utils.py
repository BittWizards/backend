import requests
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import QuerySet
from rest_framework.request import Request

from ambassadors.models import Ambassador


def send_to_ambassadors_email(
    ambassadors: QuerySet[Ambassador] | Ambassador,
    subject: str,
    message: str,
) -> int:
    """Формируем список почтовых адресов и отправляем сообщения."""
    if isinstance(ambassadors, Ambassador):
        emails = list(ambassadors.email)
    else:
        [emails.append(ambassador.email) for ambassador in ambassadors]
    return send_mail(
        subject=subject,
        message=message,
        recipient_list=emails,
        from_email=None,
    )


def send_to_ambassadors_tg(
    ambassadors: QuerySet[Ambassador] | Ambassador, message: str
) -> Request:
    """Отправляем сообщения каждому амбассадору в телеграм."""
    if not settings.BOT_TOKEN:
        return
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    if isinstance(ambassadors, Ambassador):
        if not ambassadors.tg_id:
            return
        params = {
            "chat_id": ambassadors.tg_id,
            "text": message,
        }
        requests.post(url, json=params)
    else:
        for ambassador in ambassadors:
            if ambassador.tg_id:
                params = {
                    "chat_id": ambassador.tg_id,
                    "text": message,
                }
                requests.post(url, json=params)
