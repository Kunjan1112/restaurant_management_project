from django.urls import path
from . import views

urlpatterns = [
    path('name/',views.name),

    path('index/',views.index,name='index'),

    path('login_view/',views.login_view,name='login_view'),

    path('404_view/',view.404_view,name='404_view'),
]