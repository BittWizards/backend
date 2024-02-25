def get_full_name(obj):
    """
    Возвращает полное ФИО объекта.
    """
    fio = f"{obj.last_name} {obj.first_name}"
    if obj.middle_name:
        fio = fio + f" {obj.middle_name}"
    return fio


get_full_name.short_description = "ФИО"
