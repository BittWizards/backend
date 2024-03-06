from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.views import (
    AllMerchToAmbassadorView,
    AmbassadorOrdersViewSet,
    MerchViewSet,
    OrdersViewSet,
)

router_merch = DefaultRouter()
router_merch.register("merch", MerchViewSet, basename="merch")
router_merch.register("orders", OrdersViewSet, basename="orders")

urlpatterns = [
    path(
        "ambassadors/<ambassador_id>/orders/",
        AmbassadorOrdersViewSet.as_view({"get": "retrieve"}),
        name="ambassador_orders",
    ),
    path("", include(router_merch.urls)),
    path(
        "merch_to_ambassador/",
        AllMerchToAmbassadorView.as_view(),
        name="merch_to_ambassador",
    ),
]
