from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .custom_functions import get_full_name
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "fio",
        "phone",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    def fio(self, obj):
        return get_full_name(obj)

    def save_model(self, request, obj, form, change):
        """Хэширует пароль и сохраняет его в базе данных"""
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    fio.short_description = "ФИО"
