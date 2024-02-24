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
    NOT_ACTIVE = "Not active", "Не активный"
