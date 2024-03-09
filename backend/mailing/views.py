from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from mailing.models import Message
from mailing.serializers import MessageSerializer


@extend_schema(tags=["Рассылки"])
class MessageViewSet(viewsets.ModelViewSet):
    """Viewset модели Message"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)
    http_method_names = ("get", "post", "patch", "delete")
