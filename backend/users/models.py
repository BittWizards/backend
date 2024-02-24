from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User.
    """

    def _create_user(
        self, phone: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает и сохраняет пользователя с телефоном и паролем
        """
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save()

    def create_user(
        self, phone: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает пользователя.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(
        self, phone: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает суперюзера.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone, password, **extra_fields)


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
    middle_name = models.CharField(verbose_name="Отчество", max_length=100)
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
