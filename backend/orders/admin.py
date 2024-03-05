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
        "phone",
        "country",
        "city",
        "street_home",
        "post_index",
        "full_address",
        "status",
        "created_date",
        "delivered_date",
        "track_number",
        "comment",
        "total_cost",
        "ambassador",
        "get_merch",
    )
    search_fields = ("ambassador", "merch", "status", "city")
    list_filter = ("ambassador", "merch", "status", "city")
    empty_value_display = "-пусто-"

    def get_merch(self, obj: Order) -> str:
        return ", ".join([merch.name for merch in obj.merch.all()])

    def get_ambassador(self, obj: Order) -> str:
        return Ambassador.objects.get(pk=obj.ambassador)


admin.site.register(Merch, MerchAdmin)
admin.site.register(Order, OrderAdmin)
