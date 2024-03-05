from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from ambassadors.views import (
    AmbassadorViewSet,
    YandexProgrammViewSet,
    get_ambassador_by_tg_acc,
)
from bot.views import bot_view
from content.views import (
    AllContentsViewSet,
    ContentDetailViewSet,
    PromoCodeViewSet,
)
from orders.urls import urlpatterns as orders_url

router_v1 = routers.DefaultRouter()
router_v1.register("allcontent", AllContentsViewSet, basename="allcontent")
router_v1.register("content", ContentDetailViewSet, basename="content_detail")
router_v1.register("promocodes", PromoCodeViewSet, basename="promo")
router_v1.register("ambassadors", AmbassadorViewSet, basename="ambassadors")
router_v1.register(
    r"yandexprogramms", YandexProgrammViewSet, basename="yandexprogramms"
)

v1_urlpatterns = [
    path("ambassador_by_tg_username/<str:tg_acc>/", get_ambassador_by_tg_acc),
    path("", include(router_v1.urls)),
    # С этим надо что-то делать, у нас 2 шт с одинаковыми путями
    path("", include(orders_url)),
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
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
