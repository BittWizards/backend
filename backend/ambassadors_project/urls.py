from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from orders.urls import router as orders_router

router_v1 = routers.DefaultRouter()

v1_urlpatterns = [
    path("", include(router_v1.urls)),
    path("", include(orders_router.urls)),
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
