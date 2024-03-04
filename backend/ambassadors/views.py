from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from content.models import Content, Promocode

from .models import Ambassador, YandexProgramm
from .serializers import (
    AmbassadorContentSerializer,
    AmbassadorListSerializer,
    AmbassadorPromocodeSerializer,
    AmbassadorSerializer,
    YandexProgrammSerializer,
)


@extend_schema(tags=["Амбассадоры"])
class AmbassadorViewSet(viewsets.ModelViewSet):
    """
    Viewset модели Ambassador.
    """

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorListSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_serializer_class(self):
        if self.action == "list":
            return AmbassadorListSerializer
        else:
            return AmbassadorSerializer

    @extend_schema(tags=["Контент"])
    @action(detail=False, url_path=r"(?P<ambassador_id>\d+)/contents")
    def contents(self, request, ambassador_id):
        """Весь контент амбассадора."""

        queryset = Ambassador.objects.filter(
            id=ambassador_id
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

    @extend_schema(tags=["Промокоды"])
    @action(detail=False, url_path=r"(?P<ambassador_id>\d+)/promocodes")
    def promocodes(self, request, ambassador_id):
        """Все промокоды амбассадора."""

        queryset = Ambassador.objects.filter(
            id=ambassador_id
        ).prefetch_related(
            Prefetch("my_promocode", queryset=Promocode.objects.all())
        )
        serializer = AmbassadorPromocodeSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


@extend_schema(tags=["Программы Яндекса"])
class YandexProgrammViewSet(viewsets.ModelViewSet):
    """
    Viewset модели YandexProgramm.
    """

    queryset = YandexProgramm.objects.all()
    serializer_class = YandexProgrammSerializer
    permission_classes = (AllowAny,)
