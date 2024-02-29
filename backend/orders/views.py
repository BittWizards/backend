from rest_framework import viewsets
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_201_CREATED
from django.shortcuts import get_object_or_404
from django.db.models import Q, QuerySet
from drf_spectacular.utils import extend_schema_view

from openapi.orders_schema import (orders_extend_schema_view,
                                   merch_extend_schema_view)
from orders.models import Merch, Order
from ambassadors.models import Ambassador
from orders.serializers import (
    OrderSerializer,
    MerchSerializer
)


@extend_schema_view(**orders_extend_schema_view)
class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для заявок на мерч"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self) -> QuerySet[Order]:
        ambassador_id = int(self.kwargs.get('pk'))
        query = Order.objects.filter(ambassador_id=ambassador_id)
        return query

    def get_object(self) -> Order:
        order = get_object_or_404(Order, pk=int(self.kwargs.get('pk')))
        return order

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        merch = Merch.objects.filter(
            Q(name__in=(merch.get('name') for merch in request.data['merch'])),
            Q(
                size__in=(merch.get('size') for merch in request.data['merch'])
            ) | Q(size__isnull=True)
        )
        self.perform_create(serializer, merch)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer: Serializer, merch: Merch) -> None:
        ambassador = get_object_or_404(
            Ambassador, pk=self.kwargs['pk']
        )
        serializer.validated_data['ambassador_id'] = ambassador
        serializer.save(merch=merch)

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    # TODO: Если добавить трек -> изменить статус
    # TODO: Изменение адрес в заявке
    # TODO: Если статус отправлен -> нельзя изменять заявку
    # TODO: Проверка на макс количества мерча в завке


@extend_schema_view(**merch_extend_schema_view)
class MerchViewSet(viewsets.ModelViewSet):
    """ViewSet для мерча"""
    queryset = Merch.objects.all()
    serializer_class = MerchSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
