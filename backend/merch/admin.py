from django.contrib import admin

from .models import Merch, Order


class MerchInline(admin.TabularInline):
    model = Merch
    verbose_name = "Мерч"


class MerchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "size", "cost")
    search_fields = ("name",)
    list_filter = ("name", "size", "cost")
    empty_value_display = "-пусто-"


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ambassador",
        "merch",
        "order_status",
        "created_date",
        "delivered_date",
        "track_number",
        "comment",
    )
    search_fields = ("ambassador", "merch", "order_status")
    list_filter = ("ambassador", "merch", "order_status")
    empty_value_display = "-пусто-"
    inlines = [
        MerchInline,
    ]


admin.site.register(Merch, MerchAdmin)
admin.site.register(Order, OrderAdmin)
