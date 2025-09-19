from rest_framework import serializers
from products.models import MenuCategory
from .models import ContactFormSubmission, MenuItem

class MenuCategorySerializer(serializers.ModelSerializers):

    class Meta:

        model = MenuCategory
        fields = ['id', 'name']

class ContactFormSubmissionSerializer(serializers.ModelSerializer):

    class Meta:

        model = ContactFormSubmission
        fields = ['id', 'name', 'email', 'message', 'created_at'] 
        
class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = MenuItem
        fields = ["id", "name", "description", "price", "category", "is_daily_special"]