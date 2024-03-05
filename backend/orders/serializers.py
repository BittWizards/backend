from rest_framework import serializers

from ambassadors.models import Ambassador
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


class AmbassadorShortSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения короткого списка полей амбассадора"""

    ya_programm = serializers.SerializerMethodField()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "first_name",
            "last_name",
            "middle_name",
            "status",
            "tg_acc",
            "ya_programm"
        )

    def get_ya_programm(self, obj):
        return obj.ya_programm.title


class AllOrdersListSerialiazer(serializers.ModelSerializer):
    """Сериалайзер для отображения всех существующих заявок"""

    ambassador = AmbassadorShortSerializer()

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

    merch = MerchSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "created_date", "merch", "total_cost")


class AmbassadorOrderListSerializer(serializers.ModelSerializer):
    """Сериалайзер для выдачи всех заявок на мерч по
    конкретному амбассадору. Работает только на чтение"""

    orders = OrderListSerializer(many=True)
    total_orders_cost = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    ya_programm = serializers.SerializerMethodField()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "first_name",
            "last_name",
            "middle_name",
            "city",
            "ya_programm",
            "email",
            "phone",
            "orders",
            "total_orders_cost",
        )

    def get_ya_programm(self, obj):
        return obj.ya_programm.title

    def get_city(self, obj: Ambassador) -> str:
        return obj.address.city

    def get_total_orders_cost(self, obj: Ambassador) -> int:
        return sum(order["total_cost"] or 0 for order in obj.orders.values())


class AllMerchToAmbassadorSerializer(serializers.ModelSerializer):
    """Сериалайзер для обработки всего мерча,
    который относится к конкертному амбассадору"""

    merch_name = serializers.CharField()
    count = serializers.IntegerField(default=0)
    total = serializers.IntegerField()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "image",
            "first_name",
            "last_name",
            "merch_name",
            "count",
            "total",
        )
