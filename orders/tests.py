from django.test import TestCase
from home.models import MenuItem 
from orders.models import Order, OrderItem 

# Create your tests here.

class OrderModelTest(TestCase):
    def setUp(self):
        pizza = MenuItem.objects.create(name="Pizza", price=200.00)   
        burger = MenuItem.objects.create(name="Burger", price=100.00)

        self.order = Order.objects.create()

        OrderItem.objects.create(order=self.order, menu_item=pizza, quantity=2, price=pizza.price)
        OrderItem.objects.create(order=self.order, menu_item=burger, quantity=3, price=burger.price)

    def test_calculate_total(self):
        total = self.order.calculate_total()
        self.assertEqual(total, 2*200.00 + 3*100.00) 