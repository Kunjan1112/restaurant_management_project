from django.shortcuts import render
from django.http import HttpResponse 
from django.conf import settings
from django.db import DatabaseError
from .models import Restaurant

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
    
def reservations_view(request):
    restaurant_name = getattr(settings, "RESTAURANT_NAME", "My Restaurant")
    restaurant_phone = getattr(settings, "RESTAURANT_PHONE", "Not Available")
    return render(request, 'home/reservations.html',{
        "restaurant_name":restaurant_name,
        "restaurant_phone":restaurant_phone
    })

def restaurant_list(request):
    try:
        restaurants = Restaurant.objects.all()
        return render(request,'home/restaurant_list.html', {'restaurants':restaurants})
    except DatabaseError as e:
        print(f"Database error: {e}")
        return HttpResponse("Sorry, we are having trouble loading the restaurant list at the moment.", status=500)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return HttpResponse("Something went worng. Please try again later.", status=500)
