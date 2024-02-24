from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Push
from .serializers import PushSerializer


def index(request):
    return render(request, "live/index.html")


def room(request, room_name):
    return render(request, "live/room.html", {"room_name": room_name})


class PushViewSet(viewsets.ModelViewSet):
    queryset = Push.objects.all()
    serializer_class = PushSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
