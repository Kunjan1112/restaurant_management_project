from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import DatabaseError

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from .models import Restaurant, Special, OpeningHours
from .forms import ContactForm
from .utils import generate_breadcrumbs

# Create your views here.

def generate_breadcrumbs(*args):
    return args

def name(request):
    return HttpResponse("Hello My Name is Kunjan")

def index(request):
    restaurant_name = getattr(settings, "RESTAURANT_NAME", "My Restaurant")
    restaurant_phone = getattr(settings, "RESTAURANT_PHONE", "Not Available")
    restaurant_hours = getattr(settings, "RESTAURANT_HOURS", "Mon-Fri: 11am-9pm, Sat-Sun: 10am-10pm")
    restaurant_address = getattr(settings, "RESTAURANT_ADDRESS", "123, Main Street, Ahmedabad, Gujarat, India")

    google_map_embed_url = getattr(
        settings,
        "GOOGLE_MAP_EMBED_URL",
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
    
    breadcrumbs = generate_breadcrumbs(('Home','/'))

    return render(request,'home/home.html', {
        "restaurant_name" : restaurant_name,
        "restaurant_phone" : restaurant_phone,
        "restaurant_hours" : restaurant_hours,
        "restaurant_address" : restaurant_address,
        "google_map_embed_url" : google_map_embed_url,
        "form" : form,
        "success_message" : success_message,
        "breadcrumbs" : breadcrumbs
        }
    )

def handler404(request):
    breadcrumbs = generate_breadcrumbs(('Home','/'), ('404',None))
    return render(request,'home/404.html', {'breadcrumbs':breadcrumbs}, status=404)

def login_view(request):
    breadcrumbs = generate_breadcrumbs(('Home','/'), ('Login',None))
    return render(request,'home/login.html', {'breadcrumbs':breadcrumbs})

def about_restaurant(request):
    restaurant = Restaurant.objects.first()
    breadcrumbs = generate_breadcrumbs(('Home','/'),('About',None))

    context = {
        "restaurant_name" : restaurant.name if restaurant else "My Restaurant",
        "restaurant_phone" : getattr(settings, "RESTAURANT_PHONE", "Not Available"),
        "restaurant_description" : getattr(restaurant.description if restaurant else "Our restaurant offers the best food in town.",
        "breadcrumbs" : breadcrumbs
    }

    return render(request, 'home/about.html', context)

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
                fail_silently = False
            )

            confirm_subject = "Thank you for contacting us!"
            confirm_body = (
                f"Hi {name},\n\n"
                "Thank you for reaching out to us. We have received your message "
                "and will get back to you soon.\n\n"
                "Best regards,\nYour Restaurant Team"
            )

            send_email(
                confirm_subject,
                confirm_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            message.success(request, "Thank You, Your message has been sent.")

            return redirect("thank_you_view")
    else:
        form = ContactForm()

    breadcrumbs = generate_breadcrumbs(('Home','/'), ('Contact',None))
    return render(request, 'home/contact.html',{"form":form, "breadcrumbs":breadcrumbs})

def thank_you_view(request):
    breadcrumbs = generate_breadcrumbs(('Home','/'),('Thank You',None))
    return render(request, 'home/thnak_you.html',{'breadcrumbs':breadcrumbs})

def reservations_view(request):
    restaurant_name = getattr(settings, "RESTAURANT_NAME", "My Restaurant")
    restaurant_phone = getattr(settings, "RESTAURANT_PHONE", "Not Available")
    restaurant_hours = getattr(settings, "RESTAURANT_HOURS", "Mon-Fri: 11am-9pm, Sat-Sun: 10am-10pm")
    breadcrumbs = generate_breadcrumbs(('Home','/'), ('Reservations',None))

    return render(request, 'home/reservations.html',{
        "restaurant_name":restaurant_name,
        "restaurant_phone":restaurant_phone,
        'breadcrumbs':breadcrumbs
    })

def restaurant_list(request):
    try:
        restaurants = Restaurant.objects.all()
        breadcrumbs = generate_breadcrumbs(('Home','/'), ('Restaurant',None))
        return render(request,'home/restaurant_list.html', {
            'restaurants':restaurants,
            'breadcrumbs':breadcrumbs
        })
    except DatabaseError as e:
        print(f"Database error: {e}")
        return HttpResponse("Sorry, we are having trouble loading the restaurant list at the moment.", status=500)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return HttpResponse("Something went wrong. Please try again later.", status=500)


def add_to_cart(request, item_id):
    cart = request.session.get("cart", {})
    cart[item_id] = cart.get(item_id, 0) + 1
    request.session['cart'] = cart
    return redirect("home")

def homepage(request):
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values()) if isinstance(cart, dict) else 0

    breadcrumbs = generate_breadcrumbs(('Home',None))

    specials_list = Special.objects.filter(created_at=date.today())
    paginator = Paginator(specials_list, 6)
    page_number = request.GET.get('page')
    specials = paginator.get_page(page_number)
    
    opening_hours = openingHour.objects.all()


    context = {
        'restaurant_name' : "My Awesome Restaurant",
        "cart_count" : cart_count,
        'breadcrumbs':breadcrumbs,
        'specials':specials,
        'opening_hours':opening_hours,
    }

    return render(request, "home/home.html", context)

def faq_view(request):
    breadcrumbs = generate_breadcrumbs(('Home','/'),('FAQ',None))
    return render(request, 'home/faq.html', {'breadcrumbs':breadcrumbs})

def privacy_policy(request):
    breadcrumbs = generate_breadcrumbs(('Home','/'),('Privacy Policy',None))
    return render(request,'home/privacy.html', {'breadcrumbs':breadcrumbs})

def reservations_view(request):
    return render(request, 'home/reservation.html')

def our_story(request):
    return render(request, "home/our_story.html")

def staff_view(request):
    staff_members = [
        {
            'name' : 'John Deo',
            'role' : 'Head Chef',
            'image' : 'image/staff1.jpg',
            'description' : 'John is our head chef with 15 years of culinary experinece.'
        },

        {
            'name' : 'Jane Smith',
            'role' : 'Sous Chef',
            'image' : 'image/staff2.jpg',
            'description' : 'Jane assists in the kitchen and specializes in desserts.'
        },

        {
            'name' : 'Mike Johnson',
            'role' : "Manager",
            'image' : 'image/staff3.jpg',
            'description' : 'Mike ensures that everything runs smoothly at our restaurant.'
        }
    ]

    return render(request, "home/staff.html", {"staff_members":staff_members})

def restaurant_gallery(request):
    return render(request,'home/gallery.html')

 