from drf_spectacular.utils import (
    OpenApiRequest,
    OpenApiResponse,
    extend_schema,
)
from mailing.serializers import MessageSerializer


mailing_extended_schema_view = {
    "create": extend_schema(
        summary="Создание новой рассылки",
        description="Создает новый объект рассылки",
        request={
            "post": OpenApiRequest(
                request=MessageSerializer
            )
        },
        responses={
            201: OpenApiResponse(
                description="Возвращает созданную рассылку",
                response=MessageSerializer,
            ),
            400: OpenApiResponse(description="Неправильные данные"),
        },
        tags=["Рассылки"],
    ),
    "list": extend_schema(
        summary="Получение списка всех рассылок",
        description="Возвращает список всех рассылок",
        responses={
            200: OpenApiResponse(
                description="Список рассылок",
                response=MessageSerializer,
            ),
        },
        tags=["Рассылки"],
    ),
    "retrieve": extend_schema(
        summary="Получение рассылки по ID",
        description="Возвращает объект рассылки по ID",
        responses={
            200: OpenApiResponse(
                description="Объект рассылки",
                response=MessageSerializer,
            ),
        },
        tags=["Рассылки"],
    ),
    "partial_update": extend_schema(
        summary="Частичное обновление объекта рассылки",
        description="Изменение одного или нескольких полей существующего \
            объекта рассылки",
        request={
            "post": OpenApiRequest(
                request=MessageSerializer
            )
        },
        responses={
            201: OpenApiResponse(
                description="Возвращает изменный объект рассылки",
                response=MessageSerializer,
            ),
            400: OpenApiResponse(description="Неправильные данные"),
        },
        tags=["Рассылки"],
    ),
    "destroy": extend_schema(
        summary="Удаление рассылки по ID",
        description="Удаление существующего объекта рассылки",
        responses={
            204: OpenApiResponse(description="Рассылка удалена"),
        },
        tags=["Рассылки"],
    )
}