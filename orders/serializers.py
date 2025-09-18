from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Menu


class OrderItemSerializer(serializers.ModelSerializers):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.DecimalField(source='menu_item.price', max_digits=8, decimal_places=2, read_only=True)


    class Meta:
        model = OrderItem
        fields = ["id", "menu_item_name", "menu_item_price", "quantity"]

class OrderItemSerializer(serializers.ModelSerializers):
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class OrderStatusUpdateSerializer(serializers.Serializers):
    order_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    def validate_order_id(self, value):
        if not Order.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid order ID.")
        return value