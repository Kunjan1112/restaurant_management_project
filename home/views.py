from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, JsonResponse
from django.db import DatabaseError

from django.conf import settings

from django.core.mail import send_mail

from .models import Restaurant, Special, OpeningHours, MenuItem, ContactFormSubmission, UserReview, Review, SiteSettings, Order
from .serializers import ContactFormSubmissionSerializer, MenuItemSerializer, UserReviewSerializer, RestaurantDetailsAPIView, MenuItemAvailabilitySerializer, ReviewSerializer, OpeningHoursSerializer

from .forms import ContactForm
from .utils import generate_breadcrumbs

from django.contrib import messages

from datetime import date
from django.core.paginator import Paginator
from django.db.models import Avg

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import ReviewPagination


# Create your views here.
# ----------------------------------------------------------------------------------------
def generate_breadcrumbs(cart=None):
    if cart is None:
        cart = {}

    breadcrumbs = []
    for item_id, details in cart.items():
        breadcrumbs.append(f"Item {item_id} (x{details.get('quantity',1)})")
    
    return breadcrumbs

# ------------------------------------------------------------------------------------------

def name(request):
    return HttpResponse("Hello My Name is Kunjan")

# ---------------------------------------------------------------------------------------

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

# ------------------------------------Contact View------------------------------------------------

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message_text = form.cleaned_data['message']

            subject = f"New Contact Form Submission from {name}"
            body = f"Message:\n{message}\n\nForm: {name}, Email: {email}"

            send_mail(
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
                "Address : 123 Food Street, Flavor Town\n"
                "Phone : +91-9999999999\n"
                "Email : support@myrestaurant.com\n\n"  
                "Best regards,\nYour Restaurant Team"   
            )

            send_mail(
                confirm_subject,
                confirm_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Thank you, your message has been sent.")
            return redirect("thank_you_view")
    else:
        form = ContactForm()

    breadcrumbs = generate_breadcrumbs(('Home','/'), ('Contact',None))
    return render(request, 'home/contact.html',{"form":form, "breadcrumbs":breadcrumbs})

# ----------------------------------------Thank_you_view---------------------------------

def thank_you_view(request):
    breadcrumbs = generate_breadcrumbs(('Home','/'),('Thank You',None))
    return render(request, 'home/thank_you.html',{'breadcrumbs':breadcrumbs})
 
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

# -------------------------------------------Home-Page------------------------------------------------- 

def homepage(request):
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values()) if isinstance(cart, dict) else 0

    breadcrumbs = generate_breadcrumbs(('Home',None))

    specials_list = Special.objects.filter(created_at=date.today())
    paginator = Paginator(specials_list, 6)
    page_number = request.GET.get('page')
    specials = paginator.get_page(page_number)
    
    opening_hours = openingHour.objects.all()
    settings_obj = SiteSettings.objects.first()

    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg']
    if avg_rating is not None:
        avg_rating = round(avg_rating, 1)

    recent_reviews = Review.objects.order_by('created_at')[:3]

    context = {
        'restaurant_name' : settings_obj.restaurant_name if settings_obj else "My Awesome Restaurant",
        'logo' : settings_obj.logo if settings_obj and settings_obj.logo else None,
        "cart_count" : cart_count,
        'breadcrumbs':breadcrumbs,
        'specials':specials,
        'opening_hours':opening_hours,
        'avg_rating' : avg_rating,
        'recent_reviews' : recent_reviews,
        'cuisine_type' : settings_obj.cuisine_type if settings_obj else "Cuisine Not Set",

    }

    return render(request, "home/home.html", context)

# --------------------------------------------faq_view------------------------------------------------

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

def menu(request):
    query = request.GET.get('q')
    if query:
        items = MenuItem.objects.filter(name_icontains=query)
    else:
        items = MenuItem.objects.all()
    return render(request, "home/menu.html", {"items":items, "query":query})

def location(request):
    restaurant = Restaurant.objects.first()
    return render(request, 'home/location.html', {"restaurant":restaurant})

# --------------------------view_cart-----------------------------------------

def view_cart(request):
    cart = request.session.get('cart',{})

    items = []
    total_price = 0

    for item_id, details in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id)

            if isinstance(details, dict):
                quantity = details.get("quantity",1)
            else:
                quantity = details
            
            price = menu_item.price * quantity
            total_price += price
            
            items.append({
                "id":menu_item.id,
                "name":menu_item.name,
                "price":menu_item.price,
                "quantity":quantity,
                'subtotal':price
            })
        except MenuItem.DoesNotExist:
            continue

    context = {
        'items':items,
        'total_price':total_price,
    }

    return render(request, "home/cart.html",context)

def update_cart(request, item_id):
    if request.method == "POST":
        cart = request.session.get("cart",{})
        try:
            quantity = int(request.POST.get("quantity",1))
            if quantity > 0:
                cart[str(item_id)] = {"quantity" : quantity}
                messages.success(request, "Cart updated successfully.")
            else:
                cart.pop(str(item_id), None)
                messages.info(request, "Item removed from cart.")
        except ValueError:
            messages.error(request, "Invalid quantity.")
        
        request.session['cart'] = cart
    return redirect("view cart")

def remove_from_cart(request, item_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        cart.pop(str(item_id), None)
        request.session["cart"] = cart
        messages.info(request, "Item removed from cart.")
    return redirect("view_cart")

def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.warning(request, "Your cart is empty. Please add items before chechout.")
        return redirect("view_cart")

    return render(request, 'home/checkout.html', {"cart":cart})

# ----------------------------------sitemap---------------------------------------
def sitemap_view(request):
    xml = render_to_string("sitemap.xml")
    return HttpResponse(xml, content_type="application/xml")

def careers_view(request):
    return render(request, 'careers.html')

# -----------------------------------Add TO Cart------------------------------------

def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {
            'name' : item.name,
            'price' : float(item.price),
            'quantity' : 1
        }

    request.session['cart'] = cart
    request.session.modified = True

    total = sum(v['price'] * v['quantity'] for v in cart.values())

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({'success':True, 'cart_total':total})

    message.success(request, f"{item.name} added to cart!")
    return redirect('menu')

# -------------------------------contact_thanks---------------------------------------------

def contact_thanks(request):
    return render(request, "contact_thanks.html")


# --------------------------------------home_view--------------------------------------------

def home_view(request):
    return HttpResponse("<h1>Welcome to Delicious Bites Restaurant!</h1><p>Enjoy authentic meals with your family and friends.</p>")

# -------------------------------------Menu View--------------------------------------

def menu_view(request):
    categories = dict(MenuItem.CATEGORY_CHOICES)
    grouped_items = []

    for key, label in categories.items():
        grouped_items[label] = MenuItem.objects.filter(category=key)

    return render(request, 'home/menu.html', {'grouped_items':grouped_items})

# -------------------------------------Privacy_policy------------------------------

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

# --------------------------------------Terms and Service--------------------------

def terms_service(request):
    return render(request, 'terms_service.html')

# ----------------------------------------Logout------------------------------------

def logout_view(request):
    logout(request)
    return redirect("homepage")

# -----------------------------------------news--------------------------------------

def news(request):
    return render(request, "home/news.html", {"news_items":NEWS_ITEMS})

# ------------------------------------------MenuCategory---------------------------------

from rest_framework.generics import ListAPIView
from products.models import MenuCategory
from .serializers import MenuCategorySerializer

class MenuCategoryListAPIView(ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    
# --------------------------------------------ContactFormSubmissionView-----------------------------------------

class ContactFormSubmissionView(generics.CreateAPIView):
    queryset = ContactFormSubmission.objects.all()
    serializer_class = ContactFormSubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message":"Your contact form has been submitted successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------DailySpecialsView------------------------------------

class DailySpecialsView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.filter(is_daily_special=True)

# ------------------------------------UserReviewCreateView--------------------------------------------------

class UserReviewCreateView(generics.CreateAPIView):
    queryset =  UserReview.objects.all()
    serializer_class = UserReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ------------------------------------------MenuItemReviewListView-------------------------------------------

class MenuItemReviewListView(generics.ListAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

# -------------------------------------------get_order_status--------------------------------------------

@api_view(["GET"])
def get_order_status(request, order_id):

    try:
        order = Order.objects.get(id=order_id)
        return Response(
            {"order_id":order.id, "status":order.status},
            status = status.HTTP_200_OK,
        )

    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status = status.HTTP_404_NOT_FOUND,
        )

# -------------------------------------------RestaurantDetailsAPIView-----------------------------------------------

class RestaurantDetailsAPIView(RetrieveAPIView):
    serializer_class = RestaurantSerializer

    def get_object(self):
        return Restaurant.objects.first()

# --------------------------------------------update_menu_item_availability----------------------------------------------

@api_view(['PATCH'])
def update_menu_item_availability(request, pk):

    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'error': 'MenuItem not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MenuItemAvailabilitySerializer(menu_item, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'success': f"MenuItem '{menu_item.name}' availability updated to {menu_item.is_available}"})

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------MenuItemListAPIView----------------------------------------

class MenuItemListAPIView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def list(self, request, *args, **kwargs):
        
        try: 
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)   
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 

# -----------------------------------------ReviewCreateView------------------------------------------

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# -------------------------------------------OpeningHoursView-----------------------------------

class OpeningHoursView(APIView):
    def get(self, request):
        hours = OpeningHours.objects.all()
        serializer = OpeningHoursSerializer(hours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# -------------------------------------------ReviewListView---------------------------------

class ReviewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

class ReviewListview(generics.ListAPIView):

    queryset = Review.objects.all().order_by('-created_by')
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

# --------------------------------------------MenuItemView--------------------------------------------

class MenuItemDetailsView(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get(self, request, *args, **kwargs):
        menu_item_id = kwargs.get("pk")

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found."}
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(menu_item)
        return Response(serializer.data, status=status.HTTP_200_OK)