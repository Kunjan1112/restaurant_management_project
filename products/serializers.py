from rest_framework import serializers 
from .models import Menu, MenuCategory, MenuItem, Review

# -------------------------------MenuSerializers------------------------------------------------------

class MenuSerializers(serializers.ModelSerializers):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Menu
        fields = ["id", "name", "price", "category_name"]


    def validate_price(self, value):
        if value <= 0:
            raise serializers.validationError("Price must be a positive number.")
        return value
# ------------------------------------MenuCategorySerilizers----------------------------------------------

class MenuCategorySerializer(serializers.MenuSerializers):
    class Meta:
        model = MenuCategory
        fields = ['id', 'name']

# --------------------------------------MenuItemSerializer-------------------------------------------------

class MenuItemSerializer(serializers.ModelSerializers):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price']

# ----------------------------------------ReviewSerializer--------------------------------------------

class ReviewSerializer(serializers.ModelSerializers):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'rating', 'comment', 'created_at']

        