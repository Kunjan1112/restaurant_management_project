from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuSearchViewSet, MenuCategoryListAPIView

urlpatterns = [
    path('menu/search/', MenuSearchViewSet.as_view({'get':'list'}), name='menu-search'),

    path('api/menu-categories/', MenuCategoryListAPIView.as_view(), name='menu-categories-list'),
]