from celery import shared_task

from ambassadors.models import Message
from ambassadors_project.utils import (
    send_to_ambassadors_email,
    send_to_ambassadors_tg,
)


@shared_task
def send_messages_celery(instance_id: int):
    instance = Message.objects.get(id=instance_id)
    if instance.by_email:
        send_to_ambassadors_email(
            ambassadors=instance.ambassadors.all(),
            subject=instance.title,
            message=instance.text,
        )
    if instance.to_telegram:
        send_to_ambassadors_tg(
            ambassadors=instance.ambassadors.all(), message=instance.text
        )
    return True
