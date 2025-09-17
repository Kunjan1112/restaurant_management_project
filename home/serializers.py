from rest_framework import serializers
from products.models import MenuCategory
from .models import ContactFormSubmission

class MenuCategorySerializer(serializers.ModelSerializers):
    class Meta:
        model = MenuCategory
        fields = ['id', 'name']

class ContactFormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFormSubmission
        fields = ['id', 'name', 'email', 'message', 'created_at']
        