from django.contrib import admin

from .models import Content, Screenshots, Promocode


class ScreenshotsAdmin(admin.TabularInline):
	model = Screenshots
	fields = ("screen",)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
	@admin.display(description="Доп материалы")
	def count_files(self, obj):
		if obj.screen:
			return obj.screen.count()
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
	inlines = (ScreenshotsAdmin,)


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
	list_display = (
		"ambassador",
		"promocode",
		"is_active",
		"created_at"
	)
	search_fields = (
		"ambassador",
	)
	list_filter = (
		"ambassador",
		"is_active",
	)
