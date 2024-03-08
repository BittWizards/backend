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
from orders.mixins import RetrieveMixin
from orders.models import Merch, Order, OrderStatus
from orders.serializers import (
    AllOrdersListSerialiazer,
    AmbassadorOrderListSerializer,
    MerchSerializer,
    OrderSerializer,
)
from orders.utils import editing_response_data, get_filtered_merch_objects


@extend_schema_view(**ambassador_orders_extend_schema_view)
class AmbassadorOrdersViewSet(RetrieveMixin):
    """ViewSet для заявок на мерч по конкретному амбассадору"""

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorOrderListSerializer

    def get_object(self) -> Ambassador:
        ambassador_id = self.kwargs.get("ambassador_id")
        subquery = (
            Order.objects.filter(ambassador=ambassador_id)
            .values("merch__name")
            .annotate(
                data=JSONObject(
                    id=F("id"),
                    created_date=F("created_date"),
                    name=F("merch__name"),
                    size=F("merch__size"),
                    amount=1,
                    total_cost=F("total_cost")
                )
            ).values_list("data")
        )
        return Ambassador.objects.filter(
            id=ambassador_id
        ).annotate(
            merch=ArraySubquery(subquery),
        )[0]


@extend_schema_view(**orders_extend_schema_view)
class OrdersViewSet(viewsets.ModelViewSet):
    """ViewSet для заявок на мерч"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ambassador__id", "status"]

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        serializer = AllOrdersListSerialiazer(queryset, many=True)
        return Response(serializer.data)

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
            Ambassador, pk=self.request.data["ambassador"]
        )
        serializer.validated_data["ambassador"] = ambassador
        serializer.save(merch=merch)


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
            .values("merch__name")
            .annotate(
                data=JSONObject(name=F("merch__name"), count=Count("merch"))
            )
            .values_list("data")
        )
        query = (
            Ambassador.objects.annotate(
                merch=ArraySubquery(subsuery),
                last_delivery_date=Max("orders__delivered_date"),
            )
            .filter(orders__status=OrderStatus.DELIVERED)
            .order_by("last_delivery_date")
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
        query = editing_response_data(list(query))
        return Response(query, status=HTTP_200_OK)
