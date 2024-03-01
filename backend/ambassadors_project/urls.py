from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from bot.views import bot_view
from content.views import (
    AllContentsViewSet,
    AmbassadorContentsViewSet,
    ContentDetailViewSet,
    PromoCodeViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register("allcontents", AllContentsViewSet, basename="contents")
router_v1.register("content", ContentDetailViewSet, basename="content_detail")
router_v1.register(
    r"ambassador/(?P<ambassador_id>\d+)/contents",
    AmbassadorContentsViewSet,
    basename="self_content",
)
router_v1.register("promocode", PromoCodeViewSet, basename="promo")

v1_urlpatterns = [
    path("", include(router_v1.urls)),
]
api_urlpatterns = [
    path("v1/", include(v1_urlpatterns)),
    # path("auth/", AuthAPIView.as_view(), name="registration"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
    path("tg", bot_view),
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
