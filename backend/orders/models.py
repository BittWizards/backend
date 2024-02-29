from django.core.validators import MinValueValidator
from django.db import models

from ambassadors.choices import AmbassadorsClothesSizes, AmbassadorsFootsSizes
from ambassadors.models import (AbstractAmbassador, AbstractAmbassadorAddress,
                                Ambassador)


class OrderStatus(models.TextChoices):
    """Список статусов заказа"""

    CREATED = "создано", "created"
    DELIVERED = "доставлено", "delivered"
    SHIPPED = "отправлено", "shipped"


class Merch(models.Model):
    """Модель для мерча"""
    name = models.CharField(
        verbose_name="Название продукции", max_length=60, unique=True
    )
    cost = models.IntegerField(
        verbose_name="Стоимость продукции",
        validators=[
            MinValueValidator(0, "Стоимость не может быть отрицательной"),
        ],
        default=0,
    )
    size = models.CharField(
        verbose_name="Размер для одежды",
        null=True,
        blank=True,
        choices=(
            AmbassadorsClothesSizes.choices + AmbassadorsFootsSizes.choices
        )
    )

    class Meta:
        verbose_name = "Мерч"
        verbose_name_plural = "Мерч"
        ordering = ("name", "size")

    def __str__(self):
        return f"{self.name} ({self.size})"


class Order(AbstractAmbassador, AbstractAmbassadorAddress):
    """Модель для заявки на мерч"""
    ambassador_id = models.ForeignKey(
        Ambassador,
        verbose_name="ID амбассадора",
        on_delete=models.CASCADE,
    )
    merch = models.ManyToManyField(
        Merch,
        related_name="in_order",
        verbose_name="Мерч в заявке",
    )
    order_status = models.CharField(
        verbose_name="Статус заявки",
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
    )
    created_date = models.DateField(
        verbose_name="Дата создания заявки",
        auto_now_add=True
    )
    delivered_date = models.DateField(
        verbose_name="Дата получения заказа",
        null=True,
        blank=True
    )
    track_number = models.CharField(
        verbose_name="Трек-номер",
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )
    comment = models.TextField(
        verbose_name="Комментарий к заявке",
        null=True,
        blank=True
    )
    total_cost = models.IntegerField(
        verbose_name="Полная стоимость продукции в заявке",
        validators=[
            MinValueValidator(0, "Стоимость не может быть отрицательной")
        ],
        null=True,
        blank=True,
    )
    email = models.CharField(
        verbose_name="Электронная почта", max_length=200
    )
    tg_acc = models.CharField(
        verbose_name="Телеграмм аккаунт", max_length=150
    )

    class Meta:
        verbose_name = "Заявка на отправку мерча"
        verbose_name_plural = "Заявка на отправку мерча"
        ordering = ("id",)

    @property
    def get_full_address(self):
        return '{}:{}:{}:{}'.format(
            self.country, self.city, self.street_home, self.post_index
        )
