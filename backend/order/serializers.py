from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST


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

    class Meta:
        model = Order
        fields = ('__all__')
        read_only_fields = ('created_date',)
