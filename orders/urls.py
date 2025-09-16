from django.urls import path
from . import views

urlpatterns = [
    path('order-history/', views.OrderHistroyView, name="order-histroy")
]