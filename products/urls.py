from django.urls import path
from .views import MenuCategoryView

urlpatterns = [
    path("items/", MenuCategoryView.as_view(), name="menu-by-cagtegory"),
]