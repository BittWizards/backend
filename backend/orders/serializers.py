from rest_framework import serializers

from orders.models import Merch, Order
from orders.validators import validate_merch_num


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

    def validate(self, attrs):
        merch = self.initial_data['merch']
        validate_merch_num(merch)
        attrs['merch'] = merch
        return attrs
