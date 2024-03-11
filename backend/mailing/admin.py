from django.contrib import admin

from mailing.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "sent", "is_sent")
