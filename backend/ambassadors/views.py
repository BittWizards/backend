from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Ambassador
from .serializers import AmbassadorListSerializer


class AmbassadorViewSet(viewsets.ModelViewSet):
    """
    Viewset модели Ambassador.
    """

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorListSerializer
    permission_classes = (AllowAny,)
