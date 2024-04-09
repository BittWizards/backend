import jwt
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.http.response import BadHeaderError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(("GET",))
def get_user_info(request: HttpRequest) -> Response:
    if not settings.CLIENT_SECRET:
        return Response(
            {"detail": "Yandex ID is not configured."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    token = request.headers.get("Authorization").split()
    if token[0] != "Token":
        raise BadHeaderError({"detail": "Invalid type of token."})
    try:
        user_data = jwt.decode(
            token[1], settings.CLIENT_SECRET, algorithms=["HS256"]
        )
    except Exception:
        return Response(
            {"detail": "Somethig went wrong."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return JsonResponse(user_data, status=status.HTTP_200_OK)
