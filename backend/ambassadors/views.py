from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from content.models import Content, Promocode
from orders.models import Order

from .models import Ambassador
from .serializers import (
    AmbassadorContentSerializer,
    AmbassadorListSerializer,
    AmbassadorMerchSerializer,
    AmbassadorPromocodeSerializer,
    AmbassadorSerializer,
)


@extend_schema(tags=["Амбассадоры"])
class AmbassadorViewSet(viewsets.ModelViewSet):
    """
    Viewset модели Ambassador.
    """

    queryset = Ambassador.objects.all()

    # serializer_class = AmbassadorListSerializer
    # permission_classes = (AllowAny,)
    #
    # def retrieve(self, request, pk):
    #     queryset = Ambassador.objects.all()
    #     ambassador = get_object_or_404(queryset, pk=pk)
    #     serializer = AmbassadorSerializer(ambassador)
    #     return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "list":
            return AmbassadorListSerializer
        else:
            return AmbassadorSerializer

    @action(detail=False, url_path=r"(?P<ambassador_id>\d+)/contents")
    def contents(self, request, ambassador_id):
        queryset = Ambassador.objects.filter(
            id=self.kwargs.get("ambassador_id")
        ).prefetch_related(
            Prefetch(
                "my_content",
                queryset=Content.objects.filter(
                    accepted=True
                ).prefetch_related("documents"),
            )
        )
        serializer = AmbassadorContentSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, url_path=r"(?P<ambassador_id>\d+)/promocodes")
    def promocodes(self, request, ambassador_id):
        queryset = Ambassador.objects.filter(
            id=self.kwargs.get("ambassador_id")
        ).prefetch_related(
            Prefetch("my_promocode", queryset=Promocode.objects.all())
        )
        serializer = AmbassadorPromocodeSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, url_path=r"(?P<ambassador_id>\d+)/merch")
    def merch(self, request, ambassador_id):
        queryset = Ambassador.objects.filter(
            id=self.kwargs.get("ambassador_id")
        ).prefetch_related(
            Prefetch(
                "order",
                queryset=Order.objects.filter(ambassador_id=ambassador_id),
            )
        )
        serializer = AmbassadorMerchSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
