from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User


def get_full_name(obj: "User") -> str:
    """
    Возвращает полное ФИО объекта.
    """
    fio = f"{obj.last_name} {obj.first_name}"
    if obj.middle_name:
        fio = fio + f" {obj.middle_name}"
    return fio
