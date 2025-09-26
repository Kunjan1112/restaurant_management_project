from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model 
from unittest.mock import patch
from .models import Order, OrderItem

User = get_user_model()

# -------------------------------------------OrderTotalTests-----------------------------------

class OrderTotalTests(TestCase):
    def setUp(self):
        
        self.order = Order.objects.create(
            customer = "Test Customer",
            total_amount = 0,
            status = "pending"
        )

        OrderItem.objects.create(order=self.order, name='Item 1', price=50, quantity=2)
        OrderItem.objects.create(order=self.order, name='Item 2', price=30, quantity=1)

    def test_order_items_exist(self):
        items = self.order.orderitem_set.all()
        self.assertEqual(items.count(), 2)

    def test_order_total_amount(self):
        total = sum(item.price * item.quantity for item in self.order.orderitem_set.all())
        self.assertEqual(total, 130)


# -----------------------------------------OrderModelTest----------------------------------------

class OrderModelTest(TestCase):
    def setUp(self):
        Order.objects.create(customer='Alice', total_amount=100, status="completed")
        Order.objects.create(customer='Bob', total_amount=200, status="completed")
        Order.objects.create(customer='Charlie', total_amount=50, status="pending")
        Order.objects.create(customer='David', total_amount=75, status='cancelled')

    def test_calculate_total_revenue(self):
        total_revenue = Order.calculate_total_revenue()
        self.assertEqual(total_revenue, 0)