from rest_framework import serializers


from .models import Merch, Order
from ambassador.serializers import AmbassadorSerializer


class MerchSerializer(serializers.ModelSerializer):
    """Сериалайзер для тегов"""

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
