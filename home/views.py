from django.shortcuts import render
from django.http import HttpResponse 
from django.conf import settings
# from .forms import RestaurantForm 

# Create your views here.

def name(request):
    return HttpResponse("Hello My Name is Kunjan")

def index(request):
    restaurant_name = getattr(settings, "RESTAURANT_NAME", "My Restaurant")
    restaurant_phone = getattr(settings, "RESTAURANT_PHONE", "Not Available")
    return render(request,'home/home.html', {
        "restaurant_name":restaurant_name,
        "restaurant_phone":restaurant_phone
        }
    )

def handler404(request):
    return render(request,'home/404.html', status=404)

def login_view(request):
    return render(request,'home/login.html')

def about_restaurant(request):
    restaurant_name = getattr(settings, "RESTAURANT_NAME", "My Restaurant")
    restaurant_phone = getattr(settings, "RESTAURANT_PHONE",  "Not Available")
    return render(request,'home/about.html',{
        "restaurant_name" : restaurant_name,
        "restaurant_phone" : restaurant_phone
    })

def contact_view(request):
    restaurant_phone = getattr(settings, "RESTAURANT_PHONE", "Not Available")
    return render(request,'home/contact.html',{
        "restaurant_phone" : restaurant_phone
    })
    


