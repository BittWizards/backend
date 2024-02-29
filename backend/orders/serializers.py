from rest_framework import serializers

from orders.models import Merch, Order
from orders.validators import validate_merch_num
from orders.utils import get_filtered_merch_objects


class MerchSerializer(serializers.ModelSerializer):
    """Сериалайзер для мерча"""

    class Meta:
        model = Merch
        fields = ('name', 'size')


class OrderSerializer(serializers.ModelSerializer):
    """Сериалайзер для заявок на мерч"""
    merch = MerchSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('__all__')
        read_only_fields = ('ambassador_id', 'created_date', 'order_status')

    def validate(self, attrs: dict) -> dict:
        merch = self.initial_data.get('merch')
        if merch:
            validate_merch_num(merch)
            attrs['merch'] = merch
        return attrs

    def update(self, instance: Order, validated_data: dict) -> Order:
        merch_data = validated_data.pop('merch', None)
        instance = super().update(instance, validated_data)
        if merch_data:
            merch = get_filtered_merch_objects(merch_data)
            for product in merch:
                instance.merch.add(product.id)
            instance.save()
        return instance
