from rest_framework import serializers 
from .models import Menu

class MenuSerializers(serializers.ModelSerializers):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Menu
        fields = ["id", "name", "price", "category_name"]