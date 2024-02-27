from django.contrib import admin

from .models import Content, Documents, Promocode


class DocumentsAdmin(admin.TabularInline):
    model = Documents
    fields = ("document",)


@admin.register(Documents)
class DocumentsContentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "document",
        "content_id",
    )


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    @admin.display(description="Доп материалы")
    def count_files(self, obj):
        if obj.documents:
            return obj.documents.count()
        return None

    list_display = (
        "pk",
        "ambassador",
        "created_at",
        "start_guid",
        "platform",
        "comment",
        "accepted",
        "count_files",
        "link",
    )
    search_fields = (
        "ambassador",
        "platform",
    )
    list_filter = (
        "ambassador",
        "platform",
        "accepted",
        "start_guid",
    )
    empty_value_display = "-пусто-"
    inlines = (DocumentsAdmin,)


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ("ambassador", "promocode", "is_active", "created_at")
    search_fields = ("ambassador",)
    list_filter = (
        "ambassador",
        "is_active",
    )
