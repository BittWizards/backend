import json

from channels.layers import get_channel_layer
from django.core.serializers import serialize
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Push


@receiver(post_save, sender=Push)
def my_handler(sender, instance, **kwargs):
    print("here")
    channel_layer = get_channel_layer()
    data = serialize("json", {"update": "push"})
    channel_layer.group_send(
        "test",
        {
            "type": "send.data",
            "data": json.loads(data),
        },
    )
