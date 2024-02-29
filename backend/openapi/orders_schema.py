from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiRequest, OpenApiExample
from orders.serializers import OrderSerializer

merch_example = {
    "name": "string",
    "size": "XS"
}

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
    "merch": [merch_example]
}

order_response_example = {
    "id": 0,
    "ambassador_id": 0,
    **order_request_example
}

orders_extend_schema_view = {
    "create": extend_schema(
        summary='Создание нового заказа',
        description="Создает новый заказ в базе",
        examples=[OpenApiExample(
            'post', order_request_example, request_only=True
        )],
        responses={
            201: OpenApiResponse(
                description='Возвращает созданный заказ',
                response=OrderSerializer
            ),
            400: OpenApiResponse(description='Неправильные данные'),
        },
    ),
    "retrieve": extend_schema(
        summary='Получение заявки по ID',
        description="Возвращает заявку по ID",
        responses={
            200: OpenApiResponse(
                description='Заявка по запрошенному ID',
                response=OrderSerializer
            )
        },
    ),
    "list": extend_schema(
        summary='Получение всех заявок относящихся к амбассадору по его ID',
        description="Возращает список всех заявок относящихся к амбассадору",
        responses={
            200: OpenApiResponse(
                description='Список заявок на амбассадора',
                response=OrderSerializer
            )
        }
    ),
    "partial_update": extend_schema(
        summary='Частичное обновление заявки',
        description="Изменение одного или нескольких полей существующей заявки",
        examples=[OpenApiExample(
            'patch', order_request_example, request_only=True
        )],
        responses={
            201: OpenApiResponse(
                description='Обновленная заявка',
                response=OrderSerializer
            ),
            400: OpenApiResponse(description='Неправильные данные'),
        }
    ),
    "destroy": extend_schema(
        summary='Удаление заявки по ID',
        description="Удаление уже существующей заявки",
        responses={
            204: OpenApiResponse(description="Заявка удалена"),
        }
    )
}

merch_extend_schema_view = {
    "create": extend_schema(

    ),
    "retrieve": extend_schema(

    ),
    "list": extend_schema(

    ),
    "update": extend_schema(

    ),
    "partial_update": extend_schema(

    ),
    "destroy": extend_schema(

    )
}