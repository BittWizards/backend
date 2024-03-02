from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from content.mixins import CreateRetrieveListViewSet

from .models import Ambassador
from .serializers import AmbassadorListSerializer, AmbassadorSerializer


@extend_schema(tags=["Амбассадоры"])
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
