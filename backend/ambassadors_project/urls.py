from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from ambassadors.views import (
    ActionsViewSet,
    AmbassadorActionsViewSet,
    AmbassadorAddressViewSet,
    AmbassadorSizeViewSet,
    AmbassadorViewSet,
    MessageToAmbassadorViewSet,
    SendingMessageViewSet,
    YandexProgrammViewSet,
)

router_v1 = routers.DefaultRouter()

router_v1.register(r"ambassador", AmbassadorViewSet, basename="ambassador")
router_v1.register(
    r"ambassador/(?P<ambassador_id>\d+)/actions", AmbassadorActionsViewSet
)
router_v1.register(
    r"ambassador/(?P<ambassador_id>\d+)/sizes", AmbassadorSizeViewSet
)
router_v1.register(
    r"ambassador/(?P<ambassador_id>\d+)/address", AmbassadorAddressViewSet
)
router_v1.register(
    r"ambassador/(?P<ambassador_id>\d+)/messages", MessageToAmbassadorViewSet
)
router_v1.register(r"actions", ActionsViewSet, basename="actions")
router_v1.register(
    r"yandex-programm", YandexProgrammViewSet, basename="yandex-programm"
)
router_v1.register(
    r"sending-message", SendingMessageViewSet, basename="sending-message"
)

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
