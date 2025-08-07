from django.urls import path
from . import views
urlpatterns = [
    path('name/',views.name,name="name"),
    path('index/',views.index,name="index"),
    path('login/',views.login,name="login"),

]

