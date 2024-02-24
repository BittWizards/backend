from django.contrib import admin

from .models import (
    Actions,
    Ambassador,
    AmbassadorActions,
    AmbassadorAddress,
    AmbassadorSize,
    MessageToAmbassador,
    SendingMessage,
    YandexProgramm,
)


class AmbassadorActionsTabularInline(admin.TabularInline):
    model = AmbassadorActions


class MessageToAmbassadorTabularInline(admin.TabularInline):
    model = MessageToAmbassador


@admin.register(Ambassador)
class AmbassdorAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "middle_name",
        "gender",
        "ya_programm",
        "phone",
        "tg_acc",
        "education",
        "work_now",
        "status",
        "created",
    )
    inlines = [
        AmbassadorActionsTabularInline,
        MessageToAmbassadorTabularInline,
    ]


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
        "ambassador_id",
    )


@admin.register(AmbassadorSize)
class AmbassadorSizeAdmin(admin.ModelAdmin):
    list_display = ("ambassador_id", "clothes_size", "foot_size")


@admin.register(SendingMessage)
class SendingMessageAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created", "supervisor_id", "sent")


@admin.register(MessageToAmbassador)
class MessageToAmbassadorAdmin(admin.ModelAdmin):
    list_display = ("ambassador_id", "sending_message_id")
