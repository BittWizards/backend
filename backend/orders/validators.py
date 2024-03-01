from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from ambassadors_project.constants import MERCH_MAX_NUM_IN_ORDER
from orders.models import OrderStatus


def validate_merch_num(merch: list[dict]) -> None:
    """Проверка что в заказе выбрано корректное количество мерча"""
    if not merch:
        raise ValidationError(
            "Нужно выбрать хотя бы один вид мерча", code=HTTP_400_BAD_REQUEST
        )
    if len(merch) > MERCH_MAX_NUM_IN_ORDER:
        raise ValidationError(
            f"Нельзя выбрать больше {MERCH_MAX_NUM_IN_ORDER}-х видов мерча",
            code=HTTP_400_BAD_REQUEST,
        )


def validate_editing_order(order_status: OrderStatus) -> None:
    """Проверка что заявку можно изменить"""
    if order_status != OrderStatus.CREATED:
        raise PermissionDenied(
            "Поля заявки уже нельзя изменить", code=HTTP_403_FORBIDDEN
        )
