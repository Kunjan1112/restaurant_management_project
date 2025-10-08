from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderHistroyView, OrderViewSet, UpdateOrderStatusView, OrderStatusRetrieveAPIView, UserOrderHistoryView, OrderSummaryView, TableListView


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    
    path('history/', OrderHistroyView.as_view(), name="order-histroy"),

    path('api/',include(router.urls)),

    path('api/update-status/', UpdateOrderStatusView.as_view(), name="update-order-status"),

    path('api/order/<str:unique_id>/status/', OrderStatusRetrieveAPIView.as_view(), name='order-status'),

    path('api/order/my-orders/', UserOrderHistoryView.as_view(), name="user-order-histroy"),
    
    path('api/orders/<int:pk>/summary/', OrderSummaryView.as_view(), name="order-summary"),

    path('tables/', TableListView.as_view(), name='table-list'),
]

