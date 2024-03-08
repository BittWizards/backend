from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from orders.serializers import (
    AllOrdersListSerialiazer,
    AmbassadorOrderListSerializer,
    MerchSerializer,
    OrderSerializer,
)

merch_example = {"name": "string", "size": "XS"}
order_one_request_example = {
    "ambassador": 0,
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string",
    "phone": "string",
    "country": "string",
    "city": "string",
    "street_home": "string",
    "post_index": 2147483647,
    "merch": [merch_example],
    "comment": "string",
}
order_two_request_example = {
    **order_one_request_example,
    "delivered_date": "2024-02-29",
    "track_number": "string",
}
order_response_example = {
    "id": 0,
    "created_date": "2024-02-29",
    "status": "string",
    "total_cost": 2147483647,
    **order_two_request_example,
}
orders_response_list_example = {
    "id": 0,
    "ambassador": {
        "id": 0,
        "image": "string",
        "first_name": "string",
        "last_name": "string",
        "middle_name": "string",
        "status": "string",
        "tg_acc": "string",
        "ya_programm": "string",
    },
    "track_number": 2147483647,
    "created_date": "2024-03-01",
    "status": "string",
}
all_merch_to_ambassador_example = {
    "id": 0,
    "first_name": "string",
    "last_name": "string",
    "image": "string",
    "tg_acc": "string",
    "merch": [
        {
            "name": "string",
            "count": 2147483647,
        }
    ],
    "total": 2147483647,
    "last_delivery_date": "2024-03-05",
}

ambassador_orders_extend_schema_view = {
    "retrieve": extend_schema(
        summary="Получение всех заявок относящихся к амбассадору по его ID",
        description="Возращает список всех заявок относящихся к амбассадору",
        responses={
            200: OpenApiResponse(
                description="Список заявок на амбассадора",
                response=AmbassadorOrderListSerializer,
            )
        },
        tags=["Заявки"],
    ),
}

orders_extend_schema_view = {
    "create": extend_schema(
        summary="Создание новой заявки",
        description="Создает новый заказ в базе",
        examples=[
            OpenApiExample(
                "post", order_one_request_example, request_only=True
            ),
            OpenApiExample("201", order_response_example, response_only=True),
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
    "retrieve": extend_schema(
        summary="Получение заявки по ID",
        description="Возвращает заявку по ID",
        examples=[
            OpenApiExample("200", order_response_example, response_only=True),
        ],
        responses={
            200: OpenApiResponse(
                description="Заявка по запрошенному ID",
                response=OrderSerializer,
            )
        },
        tags=["Заявки"],
    ),
    "list": extend_schema(
        summary="Получение всех существующих заявок",
        description="Возращает список всех существующих заявок,\
            доступна фильтрации по status и ambassador__id (2 нижних)",
        examples=[
            OpenApiExample(
                "200", orders_response_list_example, response_only=True
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Список всех существующих заявок",
                response=AllOrdersListSerialiazer,
            )
        },
        tags=["Заявки"],
    ),
    "partial_update": extend_schema(
        summary="Частичное обновление заявки",
        description="Изменение одного или нескольких полей существующей заявки",
        examples=[
            OpenApiExample(
                "patch",
                order_two_request_example,
                request_only=True,
                description="Можно изменить одно или несколько полей из списка",
            ),
            OpenApiExample("201", order_response_example, response_only=True),
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
    "summary": "Список всего мерча относящегося к каждому амбассадору",
    "description": "Возращает информацию мерча по каждому амбассадору",
    "responses": {
        200: OpenApiResponse(
            description="Список всего мерча по каждому амбассадору",
            response=MerchSerializer,
            examples=[
                OpenApiExample(
                    "200",
                    [all_merch_to_ambassador_example],
                    response_only=True,
                ),
            ],
        ),
    },
    "tags": ["Мерч"],
}
