from rest_framework import serializers
from .models import Order, OrderItem, Table
from products.models import Menu

# --------------------------------------------OrderItemSerializer-----------------------------------

class OrderItemSerializer(serializers.ModelSerializers):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.DecimalField(source='menu_item.price', max_digits=8, decimal_places=2, read_only=True)


    class Meta:
        model = OrderItem
        fields = ["id", "menu_item_name", "menu_item_price", "quantity"]

# ---------------------------------------------OrderItemSerializer-------------------------------------        

class OrderItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class OrderSerializer(serializers.ModelSerializers):
    items = OrderItemSerializer(many=True, source='get_items', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'items', 'total_amount', 'status']


# --------------------------------------------OrderStatusUpdateSerializer--------------------------------

class OrderStatusUpdateSerializer(serializers.Serializers):
    order_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    def validate_order_id(self, value):
        if not Order.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid order ID.")
        return value 

    def validate_order_id(self, value):
        if not Order.filter(id=value).exists():
            raise serializers.ValidationError("Order with this ID does not exist.")
        return value

# --------------------------------------------OrderStatusSerializer------------------------------------

class OrderStatusSerializer(serializers.ModelSerializers):
    class Meta:
        model = Order
        fields = ['unique_id', 'status']

# --------------------------------------------OrderSummarySerializer-----------------------------------

class OrderSummarySerializer(serializers.ModelSerializers):
    items = OrderItemSerializer(source="orderitem_set", many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total_amount', 'status', 'items']

# -----------------------------------------TableSerializer--------------------------------------

class TableSerializer(serializers.ModelSerializers):
    
    class Meta:
        model = Table
        fields = '__all__'