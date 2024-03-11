# Файл для тестирования работоспособности
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.request import Request


def index(request: Request) -> HttpResponse:
    return render(request, "live/index.html")


def room(request: Request, room_name: str) -> HttpResponse:
    return render(request, "live/room.html", {"room_name": room_name})
