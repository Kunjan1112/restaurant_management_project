from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderHistroyView, OrderViewSet, UpdateOrderStatusView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    
    path('history/', OrderHistroyView.as_view(), name="order-histroy"),

    path('',include(router.urls)),

    path('update-status/', UpdateOrderStatusView.as_view(), name="update-order-status"),
    
]