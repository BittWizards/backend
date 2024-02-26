from rest_framework import viewsets

from .models import Merch, Order
from .serializers import (
    OrderSerializer,
    MerchSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для заявок на мерч"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # TODO: Если добавить трек -> изменить статус


class MerchViewSet(viewsets.ModelViewSet):
    """ViewSet для мерча"""
    queryset = Merch.objects.all()
    serializer_class = MerchSerializer
