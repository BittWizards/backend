from drf_spectacular.utils import OpenApiResponse, extend_schema
from orders.serializers import OrderSerializer


orders_extend_schema_view = {
    "create": extend_schema(
        summary='Создание нового заказа',
        description="Создает новый заказ в базе",
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
    "update": extend_schema(
        description='Обновление всей заявки по ее ID',
        summary="Изменение всех полей заявки",
        responses={
            201: OpenApiResponse(
                description='Обновленная заявка',
                response=OrderSerializer
            ),
            400: OpenApiResponse(description='Неправильные данные'),
        }
    ),
    "partial_update": extend_schema(
        summary='Частичное обновление заявки',
        description="Изменение одного или нескольких полей заявки",
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