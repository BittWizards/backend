from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.routers import CustomOrdersRouter
from orders.views import MerchViewSet, OrderViewSet

router_orders = CustomOrdersRouter()
router_orders.register("orders", OrderViewSet, basename="orders")

router_merch = DefaultRouter()
router_merch.register("merch", MerchViewSet, basename="merch")

urlpatterns = [
    path("", include(router_orders.urls)),
    path("", include(router_merch.urls)),
]
