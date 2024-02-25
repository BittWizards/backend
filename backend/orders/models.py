from django.core.validators import MinValueValidator, MaxValueValidator
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
    size = models.CharField(
        verbose_name="Размер для одежды", choices=ClothSize, null=True
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
        through="MerchInOrder"
    )
    order_status = models.CharField(
        verbose_name="Размер для одежды",
        choices=OrderStatus,
        default=OrderStatus.CREATED,
    )
    created_date = models.DateField(
        verbose_name="Дата создания заявки", auto_now_add=True
    )
    delivered_date = models.DateField(
        verbose_name="Дата получения заказа", null=True
    )
    track_number = models.CharField(
        verbose_name="Трек-номер", max_length=20, unique=True
    )
    comment = models.CharField(verbose_name="Комментарий к заявке")

    class Meta:
        verbose_name = "Заявка на отправку мерча"
        verbose_name_plural = "Заявка на отправку мерча"
        ordering = "id"


class MerchInOrder(models.Model):
    """Модель для хранения количества мерча в заказе"""
    order = models.ForeignKey(
        Order,
        related_name="merch",
        verbose_name="Заявка для отправки мерча",
    )
    merch = models.ForeignKey(
        Merch,
        related_name="order",
        verbose_name="Мерч в заявке",
    )
    amount = models.IntegerField(
        verbose_name="Количество мерча",
        validators=[
            MinValueValidator(1, "Количество не может быть меньше 1"),
            MaxValueValidator(10, "Количество не может быть больше 10")
        ],
        default=1,
    )

    class Meta:
        verbose_name = "Мерч в заказе с количеством и общей ценой"
        verbose_name_plural = "Мерч в заказе с количеством и общей ценой"
        ordering = "id"

    @classmethod
    def total_cost(self):
        return self.merch.cost * self.amount
