from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuSearchViewSet, MenuCategoryListAPIView, MenuItemPriceRangeView, MenuItemAvailabilityView

urlpatterns = [
    path('menu/search/', MenuSearchViewSet.as_view({'get':'list'}), name='menu-search'),

    path('api/menu-categories/', MenuCategoryListAPIView.as_view(), name='menu-categories-list'),

    path('menu-items/price-range/', MenuItemPriceRangeView.as_view(), name="menu-items-price-range"),

    path('menu-items/<int:pk>/availability/', MenuItemAvailabilityView.as_view(), name="menu-item-availability"),
]