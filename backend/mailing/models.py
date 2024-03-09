from django.db import models
from django.utils import timezone

from ambassadors.models import Ambassador


class Message(models.Model):
    """
    Модель отправки сообщений.
    """

    ambassadors = models.ManyToManyField(Ambassador, related_name="messages")
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    text = models.CharField(verbose_name="Текст", max_length=2000)
    sent = models.DateTimeField(
        verbose_name="Дата отправки", null=True, default=timezone.now
    )
    by_email = models.BooleanField(verbose_name="На почту", default=False)
    to_telegram = models.BooleanField(verbose_name="В телеграм", default=False)
    is_sent = models.BooleanField(verbose_name="Отправить", default=False)

    class Meta:
        verbose_name = "Сообщение для амбассадора"
        verbose_name_plural = "Сообщения для амбассадоров"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.title}"
