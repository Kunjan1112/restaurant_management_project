from rest_framework import serializers

from products.models import MenuCategory

from .models import ContactFormSubmission, MenuItem, UserReview

class MenuCategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = MenuCategory
        fields = ['id', 'name']

# -----------------------------------------------------------------------------------------

class ContactFormSubmissionSerializer(serializers.ModelSerializer):

    class Meta:

        model = ContactFormSubmission
        fields = ['id', 'name', 'email', 'message', 'created_at'] 
        
# -----------------------------------------------------------------------------------------

class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = MenuItem
        fields = ["id", "name", "description", "price", "category", "is_daily_special"]

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