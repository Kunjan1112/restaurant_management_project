from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializers):
    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "price"]

class OrderItemSerializer(serializers.ModelSerializers):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "total_price", "items"]