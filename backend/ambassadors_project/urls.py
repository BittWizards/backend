from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from live.views import PushViewSet, index, room

router_v1 = routers.DefaultRouter()
router_v1.register(r"pushes", PushViewSet)

v1_urlpatterns = [
    path("", include(router_v1.urls)),
]
api_urlpatterns = [
    path("v1/", include(v1_urlpatterns)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
    path("", index, name="index"),
    path("<str:room_name>/", room, name="room"),
]
urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
