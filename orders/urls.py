from django.urls import path
from . import views

urlpatterns = [
    path("order/confirmation/<int:order_id>/",views.order_confirmation,name="order_confirmation"),
    path('thank-you/',views.thank_you,name="thank_you"),
]