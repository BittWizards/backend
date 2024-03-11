from django.db import models


class Gender(models.TextChoices):
    """
    Выбор гендера при создании амбассадора.
    """

    MALE = "Male", "Мужчина"
    FEMALE = "Female", "Женщина"


class AmbassadorStatus(models.TextChoices):
    """
    Выбор статуса амбассадора.
    """

    ACTIVE = "Active", "Активный"
    PAUSE = "Pause", "На паузе"
    CLARIFY = "Clarify", "Уточняется"
    NOT_ACTIVE = "Not active", "Не активный"


class AmbassadorsClothesSizes(models.TextChoices):
    """
    Выбор размера одежды амбассадора.
    """

    XS = "XS", "XS"
    S = "S", "S"
    M = "M", "M"
    L = "L", "L"
    XL = "XL", "XL"


class AmbassadorsFootsSizes(models.TextChoices):
    """
    Выбор размера обуви.
    """

    SIZE35 = "35", "35"
    SIZE36 = "36", "36"
    SIZE37 = "37", "37"
    SIZE38 = "38", "38"
    SIZE39 = "39", "39"
    SIZE40 = "40", "40"
    SIZE41 = "41", "41"
    SIZE42 = "42", "42"
    SIZE43 = "43", "43"
    SIZE44 = "44", "44"
    SIZE45 = "45", "45"


class Achievement(models.TextChoices):
    NEW = ("new", "Новичок")
    FRIEND = ("friend", "Друг практикума")
    PROFI_FRIEND = ("profi_friend", "Практикующий амбассадор")
