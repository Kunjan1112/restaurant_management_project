from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, AvaliableTablesAPIView, TableDetailAPIView, TableListAPIView, MenuItemReviewCreateView, IngredientViewSet

router = DefaultRouter()
router.register("menu-items", MenuItemViewSet, basename='menuitem') 

router.register(r'ingredients', IngredientViewSet, basename='ingredient')


urlpatterns = [

    path('name/',views.name),
 
    path('',views.index,name='index'),

    path('login_view/',views.login_view,name='login_view'),

    path('404_view/',views.handler404,name='404_view'),

    path('about_restaurant/',views.about_restaurant,name='about_restaurant'),

    path('contact/',views.contact_view,name="contact"),

    path('reservations/',views.reservations_view,name="reservations"),

    path('restaurant_list/',views.restaurant_list,name='restaurant_list'),

    path('faq/',views.faq_view,name="faq"),

    path('privacy/',views.privacy_policy,name="privacy"),

    path('thank-you/',views.thank_you_view,name="thank_you"),

    path('our-story/', views.our_story, name="our_story"),
    
    path('staff/',views.staff_view,name='staff'),

    path('restaurant-gallery/',views.restaurant_gallery,name='restaurant_gallery'),

    path('cart/',views.view_cart,name='view_cart'),

    path('sitemap/',views.sitemap_view,name="sitemap"),

    path('careers/',views.careers_view,name="careers"),

    path('contact/thanks',views.contact_thanks,name="contact_thanks"),

    path('home_view/',views.home_view,name="home_view"),
    
    path('privacy-policy/',views.privacy_policy,name="privacy_policy"),

    path('terms-service/', views.terms_service, name="terms_service"),

    path('logout_view/',views.logout_view,name="logout_view"),
    
    path('faqs/',views.FAQListView,name='faq-list'),

    path('menu-items/', views.AvaliableMenuItemsView, name="menu-items"),

    path('menu/cuisine/<str:cuisine_type>/', views.CuisineMenuItemView, name="menu-by-cuisine"),

    path('api/', include(router.urls)),

    path('api/tables/available/', AvaliableTablesAPIView.as_view(), name='available_tables_api'),

    path('api/tables/<int:pk>/', TableDetailAPIView.as_view(), name='table_detail'),

    path('api/tables/', TableListAPIView.as_view(), name='table-list'),

    path('api/cuisines/', views.CuisineMenuItemView.as_view(), name='cuisine-list'),

    path('menu-items/<int:menu_item_id>/reviews/', MenuItemReviewCreateView.as_view(), name='menu-item-review-create'),
]