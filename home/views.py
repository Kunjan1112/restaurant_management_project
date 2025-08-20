from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.db import DatabaseError

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from .models import Restaurant
from .forms import ContactForm

# Create your views here.

def name(request):
    return HttpResponse("Hello My Name is Kunjan")

def index(request):
    restaurant_name = getattr(settings, "RESTAURANT_NAME", "My Restaurant")
    restaurant_phone = getattr(settings, "RESTAURANT_PHONE", "Not Available")
    restaurant_hours = getattr(settings, "RESTAURANT_HOURS", "Mon-Fri: 11am-9pm, Sat-Sun: 10am-10pm")
    restaurant_address = getattr(settings, "RESTAURANT_ADDRESS", "123, Main Street, Ahmedabad, Gujarat, India")
    google_map_embed_url = getattr(
        settings,
        "GOOGLE_MAP_EMBED_URL"
        "#"
    )

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Thank you for contacting us!"
            form = ContactForm()
        else:
            success_message = None
    else:
        form = ContactForm()
        success_message = None

    return render(request,'home/home.html', {
        "restaurant_name" : restaurant_name,
        "restaurant_phone" : restaurant_phone,
        "restaurant_hours" : restaurant_hours,
        "restaurant_address" : restaurant_address,
        "google_map_embed_url" : google_map_embed_url,
        "form" : form,
        "success_message" : success_message,
        }
    )

def handler404(request):
    return render(request,'home/404.html', status=404)

def login_view(request):
    return render(request,'home/login.html')

def about_restaurant(request):
    restaurant_name = getattr(settings, "RESTAURANT_NAME", "My Restaurant")
    restaurant_phone = getattr(settings, "RESTAURANT_PHONE",  "Not Available")
    restaurant_hours = getattr(settings, "RESTAURANT_HOURS", "Mon-Fri: 11am-9pm, Sat-Sun: 10am-10pm")
    return render(request,'home/about.html',{
        "restaurant_name" : restaurant_name,
        "restaurant_phone" : restaurant_phone
    })

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"New Contact Form Submission from {name}"
            body = f"Message:\n{message}\n\nForm: {name}, Email: {email}"

            send_email(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently = False,
            )

            message.success(request, "Your message has been sent successfully!")
            return redirect("contact")
    else:
        form = ContactForm()
    
    return render(request, 'contact.html',{"form":form})

def reservations_view(request):
    restaurant_name = getattr(settings, "RESTAURANT_NAME", "My Restaurant")
    restaurant_phone = getattr(settings, "RESTAURANT_PHONE", "Not Available")
    restaurant_hours = getattr(settings, "RESTAURANT_HOURS", "Mon-Fri: 11am-9pm, Sat-Sun: 10am-10pm")
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


def add_to_cart(request, item_id):
    cart = request.session.get("cart", {})
    cart[item_id] = cart.get(item_id, 0) + 1
    request.session['cart'] = cart
    return redirect("home")

def homepage(request):
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())
    context = {
        'restaurant_name' : "My Awesome Restaurant",
        "cart_count" : cart_count,
    }

    return render(request, "home/home.html", context)