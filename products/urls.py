from django.urls import path
from . import views

urlpatterns = [
    path('api/menu/',views.menu_list_api,name='menu_list_api'),
    path('menu/',views.menu_view,name="menu"),
]