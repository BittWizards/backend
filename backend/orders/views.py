from django.db.models import QuerySet, Count, F
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_201_CREATED

from ambassadors.models import Ambassador
from openapi.orders_schema import (
    ambassador_orders_extend_schema_view,
    merch_extend_schema_view,
    orders_extend_schema_view,
)
from orders.models import Merch, Order
from orders.serializers import (MerchSerializer, OrderSerializer,
                                AllMerchToAmbassadorSerializer)
from orders.utils import (get_filtered_merch_objects,
                          modification_of_response_dict)


@extend_schema_view(**ambassador_orders_extend_schema_view)
class AmbassadorOrdersViewSet(viewsets.ModelViewSet):
    """ViewSet для заявок на мерч"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self) -> QuerySet[Order]:
        ambassador_id = self.kwargs.get("ambassador_id")
        return Order.objects.filter(ambassador_id=ambassador_id)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Фильтруем мерч из базы по данным из request
        merch = get_filtered_merch_objects(request.data["merch"])
        self.perform_create(serializer, merch)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer: Serializer, merch: Merch) -> None:
        ambassador = get_object_or_404(
            Ambassador, pk=self.kwargs["ambassador_id"]
        )
        serializer.validated_data["ambassador_id"] = ambassador
        serializer.save(merch=merch)

    # TODO: Если добавить трек -> изменить статус
    # TODO: Если статус отправлен -> нельзя изменять заявку
    # TODO: Добавить итоговую сумму по мерчу у амбасадора


@extend_schema_view(**orders_extend_schema_view)
class OrdersViewSet(viewsets.ModelViewSet):
    """ViewSet для заявок на мерч"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "patch", "delete"]


@extend_schema_view(**merch_extend_schema_view)
class MerchViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для мерча"""

    queryset = Merch.objects.all()
    serializer_class = MerchSerializer


class AllMerchToAmbassadorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для отображения всех амбассадоров
    и мерча который был им отправлен"""

    serializer_class = AllMerchToAmbassadorSerializer

    def get_queryset(self) -> QuerySet:
        query = Ambassador.objects.annotate(
            merch_name=F('order__merch__name'),
            count=Count("order__merch__name")
        ).order_by('id')
        return query

    def finalize_response(self, request, response, *args, **kwargs) -> Response:
        response.data = modification_of_response_dict(response.data)
        return super().finalize_response(request, response, *args, **kwargs)
