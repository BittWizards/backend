from django.contrib import admin

from .models import Merch, Order


class MerchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cost")
    search_fields = ("name",)
    list_filter = ("name", "cost")
    empty_value_display = "-пусто-"


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ambassador",
        "merch_size",
        "order_status",
        "created_date",
        "delivered_date",
        "track_number",
        "comment",
    )
    search_fields = ("ambassador", "merch", "order_status")
    list_filter = ("ambassador", "merch", "order_status")
    empty_value_display = "-пусто-"

    def get_merch(self, obj):
        return ", ".join([merch.name for merch in obj.merch.all()])


admin.site.register(Merch, MerchAdmin)
admin.site.register(Order, OrderAdmin)
