from django.shortcuts import render
from django.http import HttpResponse 
# from .forms import RestaurantForm 

# Create your views here.

def name(request):
    return HttpResponse("Hello My Name is Kunjan")

def index(request):
    restaurant_name = settings.RESTAURANT_NAME
    return render(request,'home/home.html', {"restaurant_name":restaurant_name})

def 404_view(request):
    return render(request,'home/404.html')

def login_view(request):
    return render(request,'home/login.html')


