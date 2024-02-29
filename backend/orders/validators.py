from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from orders.models import OrderStatus


def validate_merch_num(merch: list[dict]) -> None:
    """Проверка что в заказе выбрано корректное количество мерча"""
    if not merch:
        raise ValidationError(
            "Нужно выбрать хотя бы один вид мерча", code=HTTP_400_BAD_REQUEST
        )
    if len(merch) > 3:
        raise ValidationError(
            "Нельзя выбрать больше 3-х видов мерча", code=HTTP_400_BAD_REQUEST
        )


def validate_editing_order(order_status: OrderStatus) -> None:
    """Проверка что заявку можно изменить"""
    if order_status != OrderStatus.CREATED:
        raise PermissionDenied(
            "Поля заявки уже нельзя изменить", code=HTTP_403_FORBIDDEN
        )
