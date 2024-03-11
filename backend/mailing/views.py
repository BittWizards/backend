from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from mailing.models import Message
from mailing.serializers import MessageSerializer
from openapi.mailing_schema import mailing_extended_schema_view


@extend_schema_view(**mailing_extended_schema_view)
class MessageViewSet(viewsets.ModelViewSet):
    """Viewset модели Message"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)
    http_method_names = ("get", "post", "patch", "delete")
