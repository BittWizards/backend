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

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class AmbassadorsFootsSizes(models.TextChoices):
    """
    Выбор размера обуви.
    """

    LOW = "Low", "35-39"
    MEDIUM = "Medium", "39-41"
    HIGH = "High", "41-44"
    LARGE = "Large", "44-46"
