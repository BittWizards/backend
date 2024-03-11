from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from content.serializers import (
    AllContentSerializer,
    ContentSerializers,
    NewContentSerializer,
    PromocodeSerializer,
)
from ambassadors.serializers import (
    AmbassadorPromocodeSerializer,
    AmbassadorContentSerializer
)

content_request_example = {
    "link": "URLstring",
    "start_guide": True,
    "type": "review",
    "platform": "habr",
    "comment": "string",
    "accepted": True,
    "name": "string",
    "tg_acc": "string",
    "files": "URLstring"
}
promocode_request_example = {
    "promocode": "string",
    "ambassador": 0
}

promocode_extend_schema_view = {
    "create": extend_schema(
        summary="Создание нового промокода для амбассадора",
        description="Создает новый промокод для конкретного амбассадора",
        examples=[
            OpenApiExample(
                "post", promocode_request_example, request_only=True
            ),
        ],
        responses={
            201: OpenApiResponse(
                description="Возвращает новый промокод и амбассадора",
                response=PromocodeSerializer,
            ),
            400: OpenApiResponse(description="Неправильные данные"),
        },
        tags=["Промокоды"],
    ),
    "list": extend_schema(
        summary="Получение списка всех промокодов и их владельцев",
        description="Возвращает активные и не активные \
            промокоды и поля амбассадора для валадельца промокода",
        responses={
            200: OpenApiResponse(
                description="Все промокоды и их валадельцы",
                response=PromocodeSerializer,
            )
        },
        tags=["Промокоды"],
    ),
    "destroy": extend_schema(
        summary="Удаление промокода по ID",
        description="Удаление уже существующего промокода",
        responses={
            204: OpenApiResponse(description="Промокод удален"),
        },
        tags=["Промокоды"],
    )
}

all_promocodes_of_ambassador = {
    "summary": "Получение владельца и списка всех его промокодов",
    "description": "Возвращает активные и не активные \
        промокоды владельца",
    "responses": {
        200: OpenApiResponse(
            description="Владелец и все его промокоды",
            response=AmbassadorPromocodeSerializer,
        )
    },
    "tags": ["Промокоды"]
}

content_extended_schema_view = {
    "create": extend_schema(
        summary="Создание карточки нового контента",
        description="Создает карточку нового контента для амбассадора",
        examples=[
            OpenApiExample(
                "post", content_request_example, request_only=True
            ),
        ],
        responses={
            201: OpenApiResponse(
                description="Возвращает созданный заказ",
                response=ContentSerializers,
            ),
            400: OpenApiResponse(description="Неправильные данные"),
        },
        tags=["Контент"],
    ),
    "retrieve": extend_schema(
        summary="Получение контента по ID",
        description="Возвращает контент по ID",
        responses={
            201: OpenApiResponse(
                description="Возвращает контент по ID",
                response=ContentSerializers,
            ),
        },
        tags=["Контент"],
    ),
    "partial_update": extend_schema(
        summary="Частичное обновление контента",
        description="Изменение одного или нескольких полей \
            существующего контента",
        responses={
            201: OpenApiResponse(
                description="Возвращает контент по ID",
                response=ContentSerializers,
            ),
        },
        tags=["Контент"],
    ),
    "destroy": extend_schema(
        summary="Удаление контента по ID",
        description="Удаление уже существующего контента",
        responses={
            204: OpenApiResponse(description="Контент удален"),
        },
        tags=["Контент"],
    )
}
new_content_scheme = {
    "summary": "Просмотр новых заявок на контент",
    "description": "Получение всех новых заявок на контент",
    "responses": {
        200: OpenApiResponse(
            description="Возвращает спискок нового контента",
            response=NewContentSerializer(many=True)
        ),
    },
    "tags": ["Контент"],
}
allcontent_extended_schema_view = {
    "list": extend_schema(
        summary="Просмотр всего контента",
        description="Возвращает список всего контента",
        responses={
            200: OpenApiResponse(
                description="Список всего контента",
                response=AllContentSerializer
            )
        },
        tags=["Контент"],
    ),
}
allcontent_to_ambassador = {
    "summary": "Весь контент по конкретному амбассадору",
    "description": "Получение всего контента по ID амбассадора",
    "responses": {
        200: OpenApiResponse(
            description="Возвращает спискок нового контента \
                принадлежащего амбассадору",
            response=AmbassadorContentSerializer
        ),
    },
    "tags": ["Контент"],
}
