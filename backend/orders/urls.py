from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet, MerchViewSet
from orders.routers import CustomOrdersRouter


router_orders = CustomOrdersRouter()
router_orders.register('orders', OrderViewSet, basename='orders')

router_merch = DefaultRouter()
router_merch.register('merch', MerchViewSet, basename='merch')

urlpatterns = [
    path('', include(router_orders.urls)),
    path('', include(router_merch.urls)),
]
