from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from ambassadors.models import Ambassador
from ambassadors.serializers import (
    AmbassadorListSerializer,
    AmbassadorSerializer,
)
from content.mixins import CreateRetrieveListViewSet


class AmbassadorViewSet(CreateRetrieveListViewSet):
    """
    Viewset модели Ambassador.
    """

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorListSerializer
    permission_classes = (AllowAny,)

    def retrieve(self, request, pk):
        queryset = Ambassador.objects.all()
        ambassador = get_object_or_404(queryset, pk=pk)
        serializer = AmbassadorSerializer(ambassador)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "list":
            return AmbassadorListSerializer
        else:
            return AmbassadorSerializer


@extend_schema(exclude=True)
@api_view(["GET"])
def get_ambassador_by_tg_acc(request: Request, tg_acc: str) -> Response:
    """Возвращаем данные амбассадора по его username в telegram."""
    ambassador = get_object_or_404(Ambassador, tg_acc=tg_acc)
    serializer = AmbassadorSerializer(instance=ambassador)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
