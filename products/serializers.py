from rest_framework import serializers 
from .models import Menu

class MenuSerializers(serializers.ModelSerializers):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Menu
        fields = ["id", "name", "price", "category_name"]


    def validate_price(self, value):
        if value <= 0:
            raise serializers.validationError("Price must be a positive number.")
        return value