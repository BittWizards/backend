from rest_framework import serializers

from ambassadors.models import Ambassador
from ambassadors.serializers import ShortAmbassadorSerializer
from orders.models import Merch, Order, OrderStatus
from orders.utils import get_filtered_merch_objects
from orders.validators import validate_editing_order, validate_merch_num


class MerchSerializer(serializers.ModelSerializer):
    """Сериалайзер для мерча"""

    class Meta:
        model = Merch
        fields = ("name", "size")


class OrderSerializer(serializers.ModelSerializer):
    """Сериалайзер для заявок на мерч"""

    merch = serializers.SerializerMethodField()
    created_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Order
        fields = (
            "id",
            "ambassador",
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
            "created_date",
            "merch",
            "total_cost",
        )

    def get_merch(self, obj: Order):
        return obj.merch

    def validate(self, attrs: dict) -> dict:
        merch_data = self.initial_data.get("merch")
        if merch_data:
            validate_merch_num(merch_data)
            merch = get_filtered_merch_objects(merch_data)
            attrs["merch"] = merch
        return attrs

    def create(self, validated_data: dict):
        merch = validated_data.pop("merch")
        order = Order.objects.create(**validated_data)
        order.merch.add(*merch)
        return order

    def update(self, instance: Order, validated_data: dict) -> Order:
        validate_editing_order(instance.status)
        merch_data = validated_data.pop("merch", None)
        # Проверка отсутствие трек-номера у заказа
        if validated_data.get("track_number") and not instance.track_number:
            validated_data["status"] = OrderStatus.SHIPPED
        instance = super().update(instance, validated_data)
        if merch_data:
            instance.merch.clear()
            merch = get_filtered_merch_objects(merch_data)
            for product in merch:
                instance.merch.add(product.id)
            instance.save()
        return instance

    def to_representation(self, instance: Order):
        instance = super().to_representation(instance)
        instance["merch"] = MerchSerializer(instance["merch"], many=True).data
        return instance


class AllOrdersListSerialiazer(serializers.ModelSerializer):
    """Сериалайзер для отображения всех существующих заявок"""

    ambassador = ShortAmbassadorSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "ambassador",
            "track_number",
            "created_date",
            "status",
        )


class AmbassadorOrderListSerializer(serializers.ModelSerializer):
    """Сериалайзер для выдачи всех заявок на мерч по
    конкретному амбассадору. Работает только на чтение"""

    merch = serializers.SerializerMethodField()
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
            "merch",
            "total_orders_cost",
        )

    def get_merch(self, obj: Ambassador):
        return obj.merch

    def get_total_orders_cost(self, obj: Ambassador) -> int:
        return sum(order["total_cost"] or 0 for order in obj.orders.values())
