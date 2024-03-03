from rest_framework import serializers

from ambassadors.models import Ambassador
from orders.models import Merch, Order, OrderStatus
from orders.utils import get_filtered_merch_objects
from orders.validators import validate_merch_num, validate_editing_order


class MerchSerializer(serializers.ModelSerializer):
    """Сериалайзер для мерча"""

    class Meta:
        model = Merch
        fields = ("name", "size")


class OrderSerializer(serializers.ModelSerializer):
    """Сериалайзер для заявок на мерч"""

    merch = MerchSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = (
            "ambassador_id",
            "created_date",
            "order_status",
            "merch",
        )

    def validate(self, attrs: dict) -> dict:
        merch = self.initial_data.get("merch")
        if merch:
            validate_merch_num(merch)
            attrs["merch"] = merch
        return attrs

    def update(self, instance: Order, validated_data: dict) -> Order:
        validate_editing_order(instance.order_status)
        merch_data = validated_data.pop("merch", None)
        # Проверка отсутствие трек-номера у заказа
        if validated_data.get('track_number') and not instance.track_number:
            validated_data['order_status'] = OrderStatus.SHIPPED
        instance = super().update(instance, validated_data)
        if merch_data:
            instance.merch.clear()
            merch = get_filtered_merch_objects(merch_data)
            for product in merch:
                instance.merch.add(product.id)
            instance.save()
        return instance


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
            "first_name",
            "last_name",
            "merch_name",
            "count",
            "total",
        )
