from django.contrib import admin

from content.models import Content, Documents, Promocode


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
        "start_guide",
        "type",
        "accepted",
        "platform",
        "comment",
        "count_files",
        "link",
    )
    search_fields = (
        "ambassador",
        "platform",
    )
    list_filter = (
        "ambassador",
        "ambassador__achievement",
        "platform",
        "accepted",
        "start_guide",
    )
    empty_value_display = "-пусто-"
    inlines = (DocumentsAdmin,)


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ("id", "ambassador", "promocode", "is_active", "created_at")
    search_fields = ("ambassador",)
    list_filter = (
        "ambassador",
        "is_active",
    )
