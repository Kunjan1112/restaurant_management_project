from django.urls import path
from .views import *

urlpatterns = [
    path("order/confirmation/<int:order_id>/",views.order_confirmation,name="order_confirmation"),
]