from django.contrib import admin

from ambassadors.models import Ambassador
from orders.models import Merch, Order


class MerchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cost", "size")
    search_fields = ("name", "size")
    list_filter = ("name", "cost", "size")
    empty_value_display = "-пусто-"


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_full_address",
        "order_status",
        "created_date",
        "delivered_date",
        "track_number",
        "comment",
        "total_cost",
    )
    search_fields = ("ambassador_id", "merch", "order_status")
    list_filter = ("ambassador_id", "merch", "order_status")
    empty_value_display = "-пусто-"

    def get_merch(self, obj):
        return ", ".join([merch.name for merch in obj.merch.all()])

    def get_ambassador(self, obj):
        return Ambassador.objects.get(pk=obj.ambassador_id)


admin.site.register(Merch, MerchAdmin)
admin.site.register(Order, OrderAdmin)
