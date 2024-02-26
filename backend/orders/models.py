from django.core.validators import MinValueValidator
from django.db import models


class ClothSize(models.TextChoices):
    """Список размеров для одежды"""

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"


class OrderStatus(models.TextChoices):
    """Список статусов заказа"""

    CREATED = "Создано"
    DELIVERED = "Доставлено"
    SHIPPED = "Отправлено"


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
        ordering = ("name", "size")

    def __str__(self):
        return f"{self.name} {self.size}"


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
        choices=ClothSize,  # TODO добавить размеры
    )
    order_status = models.CharField(
        verbose_name="Размер для одежды",
        choices=OrderStatus,
        default=OrderStatus.CREATED,
    )
    created_date = models.DateField(
        verbose_name="Дата создания заявки",
        auto_now_add=True
    )
    delivered_date = models.DateField(
        verbose_name="Дата получения заказа",
        null=True
    )
    track_number = models.CharField(
        verbose_name="Трек-номер",
        max_length=20,
        unique=True,
        null=True
    )
    comment = models.CharField(
        verbose_name="Комментарий к заявке",
        null=True
    )

    class Meta:
        verbose_name = "Заявка на отправку мерча"
        verbose_name_plural = "Заявка на отправку мерча"
        ordering = "id"

    @property
    def total_cost(self):
        return sum(cost for merch in self.merch for cost in merch)
