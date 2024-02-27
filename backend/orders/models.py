from django.core.validators import MinValueValidator
from django.db import models

from ambassadors.models import Ambassador
from ambassadors.choices import AmbassadorsFootsSizes, AmbassadorsClothesSizes


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

    class Meta:
        verbose_name = "Мерч"
        verbose_name_plural = "Мерч"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    """Модель для заявки на мерч"""
    ambassador = models.ForeignKey(
        Ambassador,
        verbose_name="Получатель (амбассадор)",
        on_delete=models.CASCADE,
    )
    merch = models.ManyToManyField(
        Merch,
        related_name="in_order",
        verbose_name="Мерч в заявке",
    )
    merch_size = models.CharField(
        verbose_name="Размер для одежды",
        null=True,
        blank=True,
        choices=(AmbassadorsClothesSizes.choices + AmbassadorsFootsSizes.choices)
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
    comment = models.CharField(
        verbose_name="Комментарий к заявке",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Заявка на отправку мерча"
        verbose_name_plural = "Заявка на отправку мерча"
        ordering = ("id",)

    @property
    def total_cost(self):
        return sum(merch.get('cost', 0) for merch in self.merch.values())
