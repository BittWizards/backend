from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Ambassador, YandexProgramm
from .serializers import (
    AmbassadorListSerializer,
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


@extend_schema(tags=["Программы Яндекса"])
class YandexProgrammViewSet(viewsets.ModelViewSet):
    """
    Viewset модели YandexProgramm.
    """

    queryset = YandexProgramm.objects.all()
    serializer_class = YandexProgrammSerializer
    permission_classes = (AllowAny,)
