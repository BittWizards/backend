from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from .models import Merch, Order, OrderStatus
from .serializers import OrderSerializer, MerchSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для заявок на мерч"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class MerchViewSet(viewsets.ModelViewSet):
    """ViewSet для мерча"""
    queryset = Merch.objects.all()
    serializer_class = MerchSerializer