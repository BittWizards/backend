from django.db.models import Count, F, QuerySet, Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_201_CREATED

from ambassadors.models import Ambassador
from openapi.orders_schema import (
    all_merch_to_ambassador_schema_view,
    ambassador_orders_extend_schema_view,
    merch_extend_schema_view,
    orders_extend_schema_view,
)
from orders.mixins import CreateRetrieveMixin
from orders.models import Merch, Order
from orders.serializers import (
    AllMerchToAmbassadorSerializer,
    AllOrdersListSerialiazer,
    AmbassadorOrderListSerializer,
    MerchSerializer,
    OrderSerializer,
)
from orders.utils import (
    get_filtered_merch_objects,
    modification_of_response_dict,
)


@extend_schema_view(**ambassador_orders_extend_schema_view)
class AmbassadorOrdersViewSet(CreateRetrieveMixin):
    """ViewSet для заявок на мерч"""

    queryset = Order.objects.all()

    def get_object(self) -> Order:
        ambassador_id = self.kwargs.get("ambassador_id")
        return Ambassador.objects.get(id=ambassador_id)

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
        serializer.validated_data["ambassador"] = ambassador
        serializer.save(merch=merch)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderSerializer
        return AmbassadorOrderListSerializer


@extend_schema_view(**orders_extend_schema_view)
class OrdersViewSet(viewsets.ModelViewSet):
    """ViewSet для заявок на мерч"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "patch", "delete"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ambassador__id", "status"]

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        serializer = AllOrdersListSerialiazer(queryset, many=True)
        return Response(serializer.data)


@extend_schema_view(**merch_extend_schema_view)
class MerchViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для мерча"""

    queryset = Merch.objects.all()
    serializer_class = MerchSerializer


@extend_schema_view(**all_merch_to_ambassador_schema_view)
class AllMerchToAmbassadorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для отображения всех амбассадоров
    и мерча который был им отправлен"""

    serializer_class = AllMerchToAmbassadorSerializer

    def get_queryset(self) -> QuerySet:
        query = Ambassador.objects.annotate(
            merch_name=F("orders__merch__name"),
            count=Count("orders__merch__name"),
            total=Sum("orders__total_cost"),
        ).order_by("id")
        return query

    def finalize_response(
        self, request: Request, response: Response, *args, **kwargs
    ) -> Response:
        response.data = modification_of_response_dict(response.data)
        return super().finalize_response(request, response, *args, **kwargs)
