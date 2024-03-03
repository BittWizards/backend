from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from orders.serializers import (
    AllMerchToAmbassadorSerializer,
    MerchSerializer,
    OrderSerializer,
)

merch_example = {"name": "string", "size": "XS"}
order_request_example = {
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string",
    "phone": "string",
    "country": "string",
    "city": "string",
    "street_home": "string",
    "post_index": 2147483647,
    "delivered_date": "2024-02-29",
    "track_number": "string",
    "comment": "string",
    "total_cost": 2147483647,
    "email": "string",
    "tg_acc": "string",
    "merch": [merch_example],
}
order_response_example = {"id": 0, "ambassador_id": 0, **order_request_example}
all_merch_to_ambassador_example = {
    "id": 2147483647,
    "first_name": "string",
    "last_name": "string",
    "merch": {
        "string": 2147483647,
        "string": 2147483647,
        "string": 2147483647,
    },
}

ambassador_orders_extend_schema_view = {
    "create": extend_schema(
        summary="Создание новой заявки",
        description="Создает новый заказ в базе",
        examples=[
            OpenApiExample("post", order_request_example, request_only=True)
        ],
        responses={
            201: OpenApiResponse(
                description="Возвращает созданный заказ",
                response=OrderSerializer,
            ),
            400: OpenApiResponse(description="Неправильные данные"),
        },
        tags=["Заявки"],
    ),
    "list": extend_schema(
        summary="Получение всех заявок относящихся к амбассадору по его ID",
        description="Возращает список всех заявок относящихся к амбассадору",
        responses={
            200: OpenApiResponse(
                description="Список заявок на амбассадора",
                response=OrderSerializer,
            )
        },
        tags=["Заявки"],
    ),
}

orders_extend_schema_view = {
    "retrieve": extend_schema(
        summary="Получение заявки по ID",
        description="Возвращает заявку по ID",
        responses={
            200: OpenApiResponse(
                description="Заявка по запрошенному ID",
                response=OrderSerializer,
            )
        },
        tags=["Заявки"],
    ),
    "list": extend_schema(
        summary="Получение всех заявок",
        description="Возращает список всех существующих заявок",
        responses={
            200: OpenApiResponse(
                description="Список всех заявок",
                response=OrderSerializer,
            )
        },
        tags=["Заявки"],
    ),
    "partial_update": extend_schema(
        summary="Частичное обновление заявки",
        description="Изменение одного или нескольких полей существующей заявки",
        examples=[
            OpenApiExample("patch", order_request_example, request_only=True)
        ],
        responses={
            201: OpenApiResponse(
                description="Обновленная заявка", response=OrderSerializer
            ),
            400: OpenApiResponse(description="Неправильные данные"),
        },
        tags=["Заявки"],
    ),
    "destroy": extend_schema(
        summary="Удаление заявки по ID",
        description="Удаление уже существующей заявки",
        responses={
            204: OpenApiResponse(description="Заявка удалена"),
        },
        tags=["Заявки"],
    ),
}

merch_extend_schema_view = {
    "retrieve": extend_schema(
        summary="Получение мерча по ID",
        description="Возвращает мерч с размером",
        responses={
            200: OpenApiResponse(description="Мерч", response=MerchSerializer)
        },
        tags=["Мерч"],
    ),
    "list": extend_schema(
        summary="Получение всех видов мерча",
        description="Возвращает список всего мерча с размерами",
        responses={
            200: OpenApiResponse(
                description="Список всего мерча", response=MerchSerializer
            )
        },
        tags=["Мерч"],
    ),
}

all_merch_to_ambassador_schema_view = {
    "list": extend_schema(
        summary="Список всего мерча относящегося к каждому амбассадору",
        description="Возращает информацию мерча по каждому амбассадору",
        responses={
            200: OpenApiResponse(
                description="Список всего мерча по кадому амбассадору",
                response=AllMerchToAmbassadorSerializer,
            )
        },
        tags=["Мерч"],
        examples=[
            OpenApiExample(
                "200", all_merch_to_ambassador_example, response_only=True
            )
        ],
    ),
}
