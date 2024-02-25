from rest_framework.routers import DefaultRouter

from .views import (OrderViewSet, MerchViewSet)


router = DefaultRouter()
router.register('merch', MerchViewSet, basename='merch')
router.register('orders', OrderViewSet, basename='orders')
