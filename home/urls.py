from django.urls import path
from . import views

urlpatterns = [
    path('name/',views.name),

    path('',views.index,name='index'),

    path('login_view/',views.login_view,name='login_view'),

    path('404_view/',views.handler404,name='404_view'),

    path('about_restaurant/',views.about_restaurant,name='about_restaurant'),

    path('contact_view/',views.contact_view,name="contact_view"),
]