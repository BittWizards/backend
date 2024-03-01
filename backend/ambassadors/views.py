from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import (
    Actions,
    Ambassador,
    AmbassadorActions,
    AmbassadorAddress,
    AmbassadorSize,
    MessageToAmbassador,
    SendingMessage,
    YandexProgramm,
)
from .serializers import (
    ActionsSerializer,
    AmbassadorActionsSerializer,
    AmbassadorAddressSerializer,
    AmbassadorSerializer,
    AmbassadorSizeSerializer,
    MessageToAmbassadorSerializer,
    SendingMessageSerializer,
    YandexProgrammSerializer,
)


class AmbassadorViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Ambassador.
    """

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorSerializer
    permission_classes = (AllowAny,)


class YandexProgrammViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели YandexProgramm.
    """

    queryset = YandexProgramm.objects.all()
    serializer_class = YandexProgrammSerializer
    permission_classes = (AllowAny,)


class ActionsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Actions.
    """

    queryset = Actions.objects.all()
    serializer_class = ActionsSerializer
    permission_classes = (AllowAny,)


class AmbassadorActionsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели AmbassadorActions.
    """

    queryset = AmbassadorActions.objects.all()
    serializer_class = AmbassadorActionsSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        ambassador = get_object_or_404(
            Ambassador, pk=self.kwargs.get("ambassador_id")
        )
        return ambassador.actions.all()


class AmbassadorAddressViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели AmbassadorAddress.
    """

    queryset = AmbassadorAddress.objects.all()
    serializer_class = AmbassadorAddressSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        ambassador = get_object_or_404(
            Ambassador, pk=self.kwargs.get("ambassador_id")
        )
        return ambassador.address.all()


class AmbassadorSizeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели AmbassadorSize.
    """

    queryset = AmbassadorSize.objects.all()
    serializer_class = AmbassadorSizeSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        ambassador = get_object_or_404(
            Ambassador, pk=self.kwargs.get("ambassador_id")
        )
        return ambassador.sizes.all()


class SendingMessageViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели SendingMessage.
    """

    queryset = SendingMessage.objects.all()
    serializer_class = SendingMessageSerializer
    permission_classes = (AllowAny,)


class MessageToAmbassadorViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели MessageToAmbassador.
    """

    queryset = MessageToAmbassador.objects.all()
    serializer_class = MessageToAmbassadorSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        ambassador = get_object_or_404(
            Ambassador, pk=self.kwargs.get("ambassador_id")
        )
        return ambassador.messages.all()
