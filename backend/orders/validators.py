from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST


def validate_merch_num(merch: list[dict]) -> None:
    """Проверка что в заказе выбрано корректное количество мерча"""
    if not merch:
        raise ValidationError(
            'Нужно выбрать хотя бы один вид мерча',
            code=HTTP_400_BAD_REQUEST
        )
    if len(merch) > 3:
        raise ValidationError(
            'Нельзя выбрать больше 3-х видов мерча',
            code=HTTP_400_BAD_REQUEST
        )
