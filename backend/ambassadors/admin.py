from django.contrib import admin
from django.utils.safestring import mark_safe

from ambassadors.models import (
    Actions,
    Ambassador,
    AmbassadorActions,
    AmbassadorAddress,
    AmbassadorSize,
    YandexProgramm,
)
from users.custom_functions import get_full_name


class AmbassadorActionsTabularInline(admin.TabularInline):
    model = AmbassadorActions


@admin.register(Ambassador)
class AmbassdorAdmin(admin.ModelAdmin):
    @admin.display(description="Фото")
    def take_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="80" height="60">'
            )
        return None

    list_display = (
        "last_name",
        "first_name",
        "middle_name",
        "id",
        "email",
        "gender",
        "ya_programm",
        "phone",
        "tg_acc",
        "education",
        "work",
        "status",
        "created",
        "take_image",
    )
    inlines = [
        AmbassadorActionsTabularInline,
    ]

    def fio(self, instance):
        return get_full_name(instance)

    fio.short_description = "ФИО"


@admin.register(YandexProgramm)
class YandexProgrammAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


@admin.register(Actions)
class ActionsAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


@admin.register(AmbassadorAddress)
class AmbassadorAddressAdmin(admin.ModelAdmin):
    list_display = (
        "country",
        "city",
        "street_home",
        "post_index",
    )


@admin.register(AmbassadorSize)
class AmbassadorSizeAdmin(admin.ModelAdmin):
    list_display = ("clothes_size", "foot_size")
