from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ambassadors.models import Ambassador
from ambassadors.serializers import ShortAmbassadorSerializer
from orders.models import Merch, Order, OrderMerch, OrderStatus
from orders.validators import validate_editing_order


def update_merch(instance: Order, data: list[dict]) -> None:
    """Перезаписываем мерч в заявке."""
    prev_order_merch = list(instance.merch.all())
    order_merch = []
    for product in data:
        item = OrderMerch(
            merch_in_order=get_object_or_404(Merch, name=product["name"]),
            order=instance,
            size=product.get("size"),
        )
        order_merch.append(item)
    OrderMerch.objects.bulk_create(order_merch)
    for e in prev_order_merch:
        e.delete()


class MerchSerializer(serializers.ModelSerializer):
    """Сериалайзер для мерча"""

    class Meta:
        model = Merch
        fields = ("name",)


class OrderMerchSerializer(serializers.ModelSerializer):
    """Сериалайзер для мерча в заказе"""

    name = serializers.CharField(source="merch_in_order.name")
    cost = serializers.IntegerField(
        source="merch_in_order.cost", required=False
    )
    size = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = OrderMerch
        fields = ("name", "cost", "size")


class OrderSerializer(serializers.ModelSerializer):
    """Сериалайзер для заявок на мерч"""

    merch = OrderMerchSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "phone",
            "merch",
            "status",
            "created_date",
            "track_number",
            "city",
            "street_home",
            "post_index",
            "comment",
        )
        read_only_fields = (
            "ambassador",
            "created_date",
            "merch",
            "total_cost",
        )

    def create(self, validated_data: dict) -> Order:
        with transaction.atomic():
            merch_data = self.initial_data.get("merch")
            validated_data.pop("merch")
            order = Order.objects.create(**validated_data)
            order_merch = []
            for product in merch_data:
                item = OrderMerch(
                    merch_in_order=get_object_or_404(
                        Merch, name=product["name"]
                    ),
                    order=order,
                    size=product.get("size"),
                )
                order_merch.append(item)
            OrderMerch.objects.bulk_create(order_merch)
            return order

    # TODO не пропускать дальше если статус доставлено, но не передана дата
    def update(self, instance: Order, validated_data: dict) -> Order:
        validate_editing_order(instance.status)
        with transaction.atomic():
            merch_data = self.initial_data.get("merch")
            validated_data.pop("merch", None)
            # Проверка отсутствие трек-номера у заказа
            if (
                validated_data.get("track_number")
                and not instance.track_number
            ):
                validated_data["status"] = OrderStatus.SHIPPED
            instance = super().update(instance, validated_data)
            if merch_data:
                update_merch(instance, merch_data)
            return instance


class AllOrdersListSerialiazer(serializers.ModelSerializer):
    """Сериалайзер для отображения всех существующих заявок"""

    ambassador = ShortAmbassadorSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "ambassador",
            "track_number",
            "created_date",
            "status",
        )


class OrderListSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для всех заявок на мерч по
    конкретному амбассадору. Работает только на чтение.
    """

    merch = OrderMerchSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "created_date", "merch", "total_cost")


class AmbassadorOrderListSerializer(serializers.ModelSerializer):
    """Сериалайзер для выдачи всех заявок на мерч по
    конкретному амбассадору. Работает только на чтение"""

    orders = OrderListSerializer(many=True)
    total_orders_cost = serializers.SerializerMethodField()
    city = serializers.CharField(source="address.city")
    ya_programm = serializers.CharField(source="ya_programm.title")

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "first_name",
            "last_name",
            "middle_name",
            "status",
            "city",
            "ya_programm",
            "tg_acc",
            "email",
            "phone",
            "orders",
            "total_orders_cost",
        )

    def get_total_orders_cost(self, obj: Ambassador) -> int:
        return sum(order["total_cost"] or 0 for order in obj.orders.values())
