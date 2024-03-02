from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from ambassadors.models import Ambassador
from ambassadors.serializers import AmbassadorSerializer


@api_view(["GET"])
def get_ambassador_by_tg_acc(request: Request, tg_acc: str) -> Response:
    ambassador = get_object_or_404(Ambassador, tg_acc=tg_acc)
    serializer = AmbassadorSerializer(instance=ambassador)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
