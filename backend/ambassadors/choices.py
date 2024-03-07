from django.db import models


class Gender(models.TextChoices):
    """
    Выбор гендера при создании амбассадора.
    """

    MALE = "М", "Мужчина"
    FEMALE = "Ж", "Женщина"


class AmbassadorStatus(models.TextChoices):
    """
    Выбор статуса амбассадора.
    """

    ACTIVE = "Active", "Активный"
    PAUSE = "Pause", "На паузе"
    CLARIFY = "Clarify", "Уточняется"
    NOT_ACTIVE = "Not_active", "Не активный"


class AmbassadorsClothesSizes(models.TextChoices):
    """
    Выбор размера одежды амбассадора.
    """

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class AmbassadorsFootsSizes(models.IntegerChoices):
    """
    Выбор размера обуви.
    """

    SIZE35 = 35, "35"
    SIZE36 = 36, "36"
    SIZE37 = 37, "37"
    SIZE38 = 38, "38"
    SIZE39 = 39, "39"
    SIZE40 = 40, "40"
    SIZE41 = 41, "41"
    SIZE42 = 42, "42"
    SIZE43 = 43, "43"
    SIZE44 = 44, "44"
    SIZE45 = 45, "45"
