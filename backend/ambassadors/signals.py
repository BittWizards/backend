from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from ambassadors.celery_tasks import send_messages_celery
from ambassadors.models import Message


@receiver(post_save, sender=Message)
def message_handler(instance: Message, **kwargs) -> None:
    """Логика для отправки сообщений при изменении в базе данных."""
    if instance.is_sent:
        if instance.sent <= timezone.now():
            send_messages_celery.delay(instance_id=instance.id)
        else:
            send_messages_celery.apply_async(
                kwargs={"instance_id": instance.id}, eta=instance.sent
            )
