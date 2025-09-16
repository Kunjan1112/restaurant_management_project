from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuSearchViewSet

urlpatterns = [
    path('menu/search/', MenuSearchViewSet.as_view({'get':'list'}), name='menu-search'),
]