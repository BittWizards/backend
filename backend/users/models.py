from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .custom_functions import get_full_name
from .manager import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name", "phone")

    email = models.CharField(
        verbose_name="Электронная почта",
        max_length=200,
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=100, blank=False
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=100, blank=False
    )
    middle_name = models.CharField(
        verbose_name="Отчество", max_length=100, blank=True
    )
    phone = models.CharField(
        verbose_name="Номер телефона",
        max_length=15,
        blank=False,
    )
    is_staff = models.BooleanField(
        "Стафф статус",
        default=False,
    )
    is_superuser = models.BooleanField(
        "Super статус",
        default=False,
    )
    is_active = models.BooleanField(
        "Активный пользователь",
        default=False,
    )

    objects = MyUserManager()

    class Meta:
        ordering = ("id",)
        unique_together = ("email", "phone")
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def get_full_name(self):
        return get_full_name(self)
