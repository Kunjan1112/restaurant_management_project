from rest_framework import serializers
from products.models import MenuCategory

class MenuCategorySerializer(serializers.ModelSerializers):
    class Meta:
        model = MenuCategory
        fields = ['id', 'name']