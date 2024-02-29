from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from ambassadors.models import Ambassador
from openapi.orders_schema import (merch_extend_schema_view,
                                   orders_extend_schema_view)
from orders.models import Merch, Order
from orders.serializers import MerchSerializer, OrderSerializer
from orders.utils import get_filtered_merch_objects


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
        # Фильтруем мерч из базы по данным из request
        merch = get_filtered_merch_objects(request.data['merch'])
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

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        order = get_object_or_404(Order, pk=kwargs['pk'])
        self.perform_destroy(order)
        return Response(status=HTTP_204_NO_CONTENT)

    # TODO: Если добавить трек -> изменить статус
    # TODO: Если статус отправлен -> нельзя изменять заявку


@extend_schema_view(**merch_extend_schema_view)
class MerchViewSet(viewsets.ModelViewSet):
    """ViewSet для мерча"""
    queryset = Merch.objects.all()
    serializer_class = MerchSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
