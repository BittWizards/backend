from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import Count, F, Max, OuterRef, Sum
from django.db.models.functions import JSONObject
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import views, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from ambassadors.models import Ambassador
from openapi.orders_schema import (
    all_merch_to_ambassador_schema_view,
    ambassador_orders_extend_schema_view,
    merch_extend_schema_view,
    orders_extend_schema_view,
)
from orders.mixins import CreateRetrieveMixin
from orders.models import Merch, Order, OrderStatus
from orders.serializers import (
    AllOrdersListSerialiazer,
    AmbassadorOrderListSerializer,
    MerchSerializer,
    OrderSerializer,
)
from orders.utils import get_filtered_merch_objects


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


@extend_schema(**all_merch_to_ambassador_schema_view)
class AllMerchToAmbassadorView(views.APIView):
    """View для отображения всех амбассадоров
    и мерча который был им отправлен"""

    def get(self, request: Request) -> Response:
        subsuery = (
            Order.objects.filter(ambassador=OuterRef("pk"))
            .values("merch")
            .annotate(
                data=JSONObject(
                    merch_name=F("merch__name"), count=Count("merch__name")
                )
            )
            .values_list("data")
        )
        query = (
            Ambassador.objects.annotate(
                merch=ArraySubquery(subsuery),
                last_delivery_date=Max("orders__delivered_date"),
                merch_count=Count("merch", distinct=True),
            )
            .filter(orders__status=OrderStatus.CREATED)
            .order_by("merch_count")
            .annotate(total=Sum("orders__total_cost", distinct=True))
            .values(
                "id",
                "first_name",
                "last_name",
                "image",
                "tg_acc",
                "merch",
                "last_delivery_date",
                "total",
            )
        )
        return Response(list(query), status=HTTP_200_OK)
