from django.shortcuts import render
from django.http import HttpResponse 
from django.conf import settings
# from .forms import RestaurantForm 

# Create your views here.

def name(request):
    return HttpResponse("Hello My Name is Kunjan")

def index(request):
    restaurant_name = getattr(settings, "RESTAURANT_NAME", "My Restaurant")
    return render(request,'home/home.html', {"restaurant_name":restaurant_name})

def 404_view(request):
    return render(request,'home/404.html')

def login_view(request):
    return render(request,'home/login.html')

def about_restaurant(request):
    return render(request,'home/about.html')


