from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuCategoryView

router = DefaultRouter()
router.register(r"search", MenuSearchViewSet, basename="menu-search")

urlpatterns = [
    path("", include(router.urls)),
]