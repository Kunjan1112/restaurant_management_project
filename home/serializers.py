from rest_framework import serializers

from products.models import MenuCategory

from .models import ContactFormSubmission, MenuItem, UserReview, Restaurant, OpeningHour, FAQ, Table, Cuisine

# ----------------------------------------------------------------------------------------

class MenuCategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = MenuCategory 
        fields = ['id', 'name', 'description']

# -----------------------------------------------------------------------------------------

class ContactFormSubmissionSerializer(serializers.ModelSerializer):

    class Meta:

        model = ContactFormSubmission
        fields = ['id', 'name', 'email', 'message', 'created_at'] 
        
# -----------------------------------------------------------------------------------------

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category']

# -----------------------------------------------------------------------------------------

class UserReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = UserReview
        fields = ['id', 'user', 'menu_item', 'rating', 'comment', 'review_date']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

# ---------------------------------------------------------------------------------------

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant 
        fields = ['id', 'name', 'address', 'phone_number', 'opening_hours', 'email', 'description']

# ---------------------------------------------------------------------------------------

class MenuItemAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'is_available']

# -------------------------------------------------ReviewSerializer---------------------------------------

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'text', 'created_at']

        def validate_rating(self, value):
            if value < 1 or value > 5:
                raise serializers.ValidationError("Rating must be between 1 and 5.")
            return value

# ----------------------------------------opening_hours_serializer-------------------------------------

class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        fields = ['day', 'open_time', 'close_time']

# -----------------------------------------FAQSerializer----------------------------------------------

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at']

# -------------------------------------------TableSerializer-------------------------------------------

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['table_number', 'capacity', 'is_available']
        
# ---------------------------------------------CuisineSerializer-------------------------------------

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id', 'name']

