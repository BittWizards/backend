from rest_framework import serializers


from .models import Merch, Order
from ambassadors.serializers import AmbassadorSerializer


class MerchSerializer(serializers.ModelSerializer):
    """Сериалайзер для мерча"""

    class Meta:
        model = Merch
        fields = ('__all__')


class OrderSerializer(serializers.ModelSerializer):
    """Сериалайзер для заявок на мерч"""
    ambassador = AmbassadorSerializer()
    merch = MerchSerializer(many=True)

    class Meta:
        model = Order
        fields = ('__all__')
        read_only_fields = ('created_date', 'order_status')
