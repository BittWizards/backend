from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from users import custom_functions
from users.models import AbstractUser

from .choices import (
    AmbassadorsClothesSizes,
    AmbassadorsFootsSizes,
    AmbassadorStatus,
    Gender,
)

User = get_user_model()


class AbstractAmbassador(AbstractUser):
    """Абстрактная модель амбассадора с полями Имя, Фамилия, Отечство,
    Почта, Телефон, Телеграм."""

    tg_acc = models.CharField(
        verbose_name="Телеграмм аккаунт", max_length=150, unique=True
    )

    class Meta:
        abstract = True


class AbstractAmbassadorAddress(models.Model):
    """Абстрактный класс для адреса амбассадора."""

    country = models.CharField(verbose_name="Страна", max_length=100)
    city = models.CharField(verbose_name="Город", max_length=100)
    street_home = models.CharField(verbose_name="Улица", max_length=200)
    post_index = models.IntegerField(
        verbose_name="Индекс",
    )

    class Meta:
        abstract = True


class YandexProgramm(models.Model):
    """
    Модель курса Яндекса.
    """

    title = models.CharField(verbose_name="заголовок", max_length=300)
    description = models.CharField(verbose_name="Описание", max_length=1000)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("id",)

    def __str__(self) -> str:
        return str(self.title)


class Ambassador(AbstractAmbassador):
    """
    Модель амбассадора.
    """

    gender = models.CharField(
        verbose_name="Пол", max_length=20, choices=Gender.choices
    )
    ya_programm = models.ForeignKey(
        YandexProgramm,
        verbose_name="Текущий курс",
        on_delete=models.SET_NULL,
        null=True,
    )
    education = models.CharField(verbose_name="Образование", max_length=1500)
    work = models.CharField(verbose_name="Работа", blank=True, null=True)
    status = models.CharField(
        verbose_name="Статус", max_length=50, choices=AmbassadorStatus.choices
    )
    created = models.DateTimeField(
        verbose_name="Дата и время создания", default=timezone.now
    )
    tg_id = models.IntegerField(
        verbose_name="Телеграмм id", blank=True, null=True
    )
    image = models.ImageField(
        "Фото",
        upload_to="profiles/",
        null=True,
        default="profiles/default_pic.jpeg",
    )

    class Meta:
        verbose_name = "Амбассадор"
        verbose_name_plural = "Амбассадоры"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def get_full_name(self):
        return custom_functions.get_full_name(self)


class Actions(models.Model):
    """
    Действия для амбассадоров.
    """

    title = models.CharField(verbose_name="Заголовок", max_length=150)
    description = models.CharField(verbose_name="Описание", max_length=2000)

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"
        ordering = ("id",)

    def __str__(self) -> str:
        return self.title


class AmbassadorActions(models.Model):
    """
    Связанная таблица Ambassador и Actions.
    """

    ambassador_id = models.ForeignKey(
        Ambassador,
        verbose_name="Амбассадор",
        on_delete=models.CASCADE,
        related_name="actions",
    )
    action = models.ForeignKey(
        Actions,
        verbose_name="Действие",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "Действие амбассадора"
        verbose_name_plural = "Действия амбассадоров"
        ordering = ("id",)


class AmbassadorAddress(AbstractAmbassadorAddress):
    """
    Модель адреса амбассадора.
    """

    ambassador_id = models.OneToOneField(
        Ambassador,
        verbose_name="Амбассадор",
        on_delete=models.CASCADE,
        related_name="address",
    )

    class Meta:
        verbose_name = "Адрес амбассадора"
        verbose_name_plural = "Адреса амбассадоров"
        ordering = ("id",)

    def __str__(self) -> str:
        return (
            f"{self.country} {self. city} {self.street_home} {self.post_index}"
        )


class AmbassadorSize(models.Model):
    """
    Таблица размеров амбассадоров.
    """

    ambassador_id = models.OneToOneField(
        Ambassador,
        verbose_name="Амбассадор",
        on_delete=models.CASCADE,
        related_name="size",
    )

    clothes_size = models.CharField(
        verbose_name="Размер одежды",
        max_length=30,
        choices=AmbassadorsClothesSizes.choices,
    )
    foot_size = models.IntegerField(
        verbose_name="Размер обуви",
        choices=AmbassadorsFootsSizes.choices,
    )

    class Meta:
        verbose_name = "Размеры амбассадора"
        verbose_name_plural = "Размеры амбассадоров"
        ordering = ("id",)

    def __str__(self) -> str:
        return (
            f"Размер обуви:{self.foot_size}, размер одежды:{self.clothes_size}"
        )


class SendingMessage(models.Model):
    """
    Модель отправки сообщений.
    """

    title = models.CharField(verbose_name="Заголовок", max_length=100)
    description = models.CharField(verbose_name="Описание", max_length=2000)
    created = models.DateTimeField(verbose_name="Было отправлено", null=True)
    supervisor_id = models.ForeignKey(
        User, verbose_name="Супервизор", on_delete=models.CASCADE
    )
    sent = models.BooleanField(verbose_name="Отправлено", default=False)

    class Meta:
        verbose_name = "Сообщение для амбассадора"
        verbose_name_plural = "Сообщения для амбассадоров"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.title}"


class MessageToAmbassador(models.Model):
    """
    Связанная таблица сообщений и амбассадоров.
    """

    ambassador_id = models.ForeignKey(
        Ambassador,
        verbose_name="Амбассадор",
        on_delete=models.SET_NULL,
        null=True,
    )
    sending_message_id = models.ForeignKey(
        SendingMessage,
        verbose_name="Сообщение",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "Отправленное сообщение для амбассадора"
        verbose_name_plural = "Отправленные сообщения для амбассадоров"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.ambassador_id} {self.sending_message_id}"
