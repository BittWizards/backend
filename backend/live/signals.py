from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Push


@receiver(post_save, sender=Push)
def my_handler(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "test",
        {
            "type": "chat.message",
            "message": "push",
        },
    )
