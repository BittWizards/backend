from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view

from openapi.orders_schema import (orders_extend_schema_view,
                                   merch_extend_schema_view)
from .models import Merch, Order
from .serializers import (
    OrderSerializer,
    MerchSerializer
)


@extend_schema_view(**orders_extend_schema_view)
class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для заявок на мерч"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # TODO: Если добавить трек -> изменить статус


@extend_schema_view(**merch_extend_schema_view)
class MerchViewSet(viewsets.ModelViewSet):
    """ViewSet для мерча"""
    queryset = Merch.objects.all()
    serializer_class = MerchSerializer
