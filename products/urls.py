from django.urls import path
from . import views

urlpatterns = [
    path('menu_list_api/',views.menu_list_api,name='menu_list_api'),
]