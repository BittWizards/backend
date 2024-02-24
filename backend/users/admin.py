from django.contrib import admin

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
        fi = f"{obj.last_name} {obj.first_name}"
        if obj.middle_name:
            fi = f"{obj.last_name} {obj.first_name} {obj.middle_name}"
        return fi

    fio.short_description = "ФИО"
