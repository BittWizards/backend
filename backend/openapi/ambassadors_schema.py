from drf_spectacular.utils import (
    OpenApiResponse,
    OpenApiRequest,
    extend_schema,
)
from ambassadors.serializers import (
    AmbassadorListSerializer,
    AmbassadorSerializer,
    YandexProgrammSerializer,
    FormCreateAmbassadorSerializer
)

ambassador_extend_schema_view = {
    "create": extend_schema(
        summary="Создание нового амбассадора",
        description="Создает объект амбассадора",
        request={
            "post": OpenApiRequest(
                request=AmbassadorSerializer
            )
        },
        responses={
            201: OpenApiResponse(
                description="Возвращает новго амбассадора",
                response=AmbassadorSerializer,
            ),
            400: OpenApiResponse(description="Неправильные данные"),
        },
        tags=["Амбассадоры"],
    ),
    "list": extend_schema(
        summary="Получение списка всех амбассадоров",
        description="Возвращает список всех амбассадоров с ограниченными \
            полями амбассадора, доступна фильтарция по статусу амбассадора",
        responses={
            200: OpenApiResponse(
                description="Список амбассадоров",
                response=AmbassadorListSerializer,
            ),
        },
        tags=["Амбассадоры"],
    ),
    "retrieve": extend_schema(
        summary="Получение амбассадора по ID",
        description="Возвращает объект амбассадора",
        responses={
            200: OpenApiResponse(
                description="Объект амбассадора",
                response=AmbassadorSerializer,
            ),
        },
        tags=["Амбассадоры"],
    ),
    "partial_update": extend_schema(
        summary="Частичное обновление объекта амбассадор",
        description="Изменение одного или нескольких полей существующего \
            объекта амбассадора",
        request={
            "post": OpenApiRequest(
                request=AmbassadorSerializer
            )
        },
        responses={
            201: OpenApiResponse(
                description="Возвращает изменного амбассадора",
                response=AmbassadorSerializer,
            ),
            400: OpenApiResponse(description="Неправильные данные"),
        },
        tags=["Амбассадоры"],
    ),
    "destroy": extend_schema(
        summary="Удаление амбассадора по ID",
        description="Удаление существующего амбассадора",
        responses={
            204: OpenApiResponse(description="Амбассадор удален"),
        },
        tags=["Амбассадоры"],
    )
}
form_create_schema = {
    "summary": "Создание объекта амбассадора через Яндекс форму",
    "description": "Возращает объект амбассадора",
    "request": {
        "post": OpenApiRequest(
            request=FormCreateAmbassadorSerializer
        )
    },
    "responses": {
        201: OpenApiResponse(
            description="Возвращает новый объект амбассадора",
            response=FormCreateAmbassadorSerializer,
        ),
    },
    "tags": ["Амбассадоры"],
}

yandex_programms_extend_schema_view = {
    "list": extend_schema(
        summary="Получение списка всех программ Яндекса",
        description="Возвращает список всех программ Яндекса",
        responses={
            200: OpenApiResponse(
                description="Список программ Яндекса",
                response=YandexProgrammSerializer,
            ),
        },
        tags=["Программы Яндекса"],
    )
}