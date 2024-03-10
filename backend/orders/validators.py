from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from ambassadors_project.constants import (
    DELIVERED_STATUS_WITHOUT_DATE_ERROR,
    MERCH_MAX_NUM_IN_ORDER,
)
from orders.models import Merch, OrderStatus


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


def validate_editing_order(order_status: str) -> None:
    """Проверка что заявка не в статусе Delivered"""
    if order_status == OrderStatus.DELIVERED:
        raise PermissionDenied(
            "Заявка выполнена и поля заявки уже нельзя изменить",
            code=HTTP_403_FORBIDDEN,
        )


def validate_exsisting_merch(merch: Merch | None) -> None:
    """Проверка что есть такой мерч"""
    if not merch:
        raise ValidationError(
            "Добавлен несуществующий мерч", code=HTTP_400_BAD_REQUEST
        )


def validate_delivered_date(data: dict) -> None:
    if "status" in data and data["status"] == "delivered":
        if "delivered_date" not in data:
            raise ValidationError(DELIVERED_STATUS_WITHOUT_DATE_ERROR, 400)
