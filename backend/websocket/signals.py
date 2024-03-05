from ambassadors.models import Ambassador
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from content.models import Content
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Ambassador)
def new_ambassador_handler(**kwargs) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification",
        {
            "type": "chat.message",
            "message": "ambassador",
        },
    )


@receiver(post_save, sender=Content)
def new_content_handler(**kwargs) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification",
        {
            "type": "chat.message",
            "message": "content",
        },
    )
