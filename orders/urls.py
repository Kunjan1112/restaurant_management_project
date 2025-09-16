from django.urls import path
from .views import OrderHistroyView

urlpatterns = [
    path('history/', OrderHistroyView.as_view(), name="order-histroy"),
]