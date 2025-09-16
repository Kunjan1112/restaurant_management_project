from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuCategoryView

# router = DefaultRouter()
# router.register(r"menu-items", MenuViewSet, basename="menu")

urlpatterns = [
    path("items/", MenuCategoryView.as_view(), name="menu-by-cagtegory"),
]