from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status

from .models import Ambassador
from .serializers import AmbassadorListSerializer, AmbassadorSerializer


class AmbassadorViewSet(viewsets.ModelViewSet):
    """
    Viewset модели Ambassador.
    """

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorListSerializer
    permission_classes = (AllowAny,)

    @action(
        methods=("get",),
        url_path=r"(?P<pk>\d+)",
        detail=False,
        permission_classes=(AllowAny,),
    )
    def ambassadors_list(self, request, pk):
        try:
            ambassador = Ambassador.objects.get(id=pk)
            serializer = AmbassadorSerializer(ambassador)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
