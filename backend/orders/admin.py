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
        "first_name",
        "last_name",
        "middle_name",
        "email",
        "phone",
        "tg_acc",
        "country",
        "city",
        "street_home",
        "post_index",
        "full_address",
        "order_status",
        "created_date",
        "delivered_date",
        "track_number",
        "comment",
        "total_cost",
    )
    search_fields = ("ambassador_id", "merch", "order_status", "city")
    list_filter = ("ambassador_id", "merch", "order_status", "city")
    empty_value_display = "-пусто-"

    def get_merch(self, obj: Order) -> str:
        return ", ".join([merch.name for merch in obj.merch.all()])

    def get_ambassador_id(self, obj: Order) -> str:
        return Ambassador.objects.get(pk=obj.ambassador_id)


admin.site.register(Merch, MerchAdmin)
admin.site.register(Order, OrderAdmin)
