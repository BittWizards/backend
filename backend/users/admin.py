from django.contrib import admin

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

    fio.short_description = "ФИО"
