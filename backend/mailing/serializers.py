from typing import Sequence

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from ambassadors.models import Ambassador
from ambassadors.serializers import AmbassadorInMessageSerializer
from mailing.models import Message


def check_ambassadors(data: Sequence) -> list:
    ambassadors_id = [amb["id"] for amb in data]
    ambassadors = Ambassador.objects.filter(id__in=(ambassadors_id))
    if len(ambassadors) != len(ambassadors_id):
        raise ValidationError(
            "Абмассадора с таким id не существует", code=HTTP_404_NOT_FOUND
        )
    return ambassadors_id


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели сообщений."""

    ambassadors = AmbassadorInMessageSerializer(many=True)
    sent = serializers.DateTimeField(required=False, allow_null=True)
    by_email = serializers.BooleanField(required=False)
    to_telegram = serializers.BooleanField(required=False)
    is_sent = serializers.BooleanField(required=False)

    class Meta:
        model = Message
        fields = (
            "id",
            "title",
            "text",
            "sent",
            "by_email",
            "to_telegram",
            "is_sent",
            "ambassadors",
        )

    def create(self, validated_data: dict) -> Message:
        ambassadors_data = validated_data.pop("ambassadors")
        with transaction.atomic():
            instance = Message.objects.create(**validated_data)
            ambassadors_id = check_ambassadors(ambassadors_data)
            instance.ambassadors.set(ambassadors_id)
        return instance

    def update(self, instance: Message, validated_data: dict) -> Message:
        ambassadors_data = validated_data.pop("ambassadors", None)
        if instance.is_sent:
            raise ValidationError(
                "Это сообщение уже нельзя изменить.", code=HTTP_403_FORBIDDEN
            )
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            if ambassadors_data:
                ambassadors_id = check_ambassadors(ambassadors_data)
                instance.ambassadors.set(ambassadors_id)
            instance.save()
        return instance
