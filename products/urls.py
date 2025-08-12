from django.urls import path
from . import views

urlpatterns = [
    path('menu_list/',views.menu_list,name='menu_list'),
]