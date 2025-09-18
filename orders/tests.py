from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from .models import Order, OrderItem

User = get_user_model()

class OrderTotalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u1", password="pass")
        self.order = Order.objects.create(customer=self.user)

    def test_empty_order_total_is_zero(self):
        self.assertEqual(self.order.calculate_total(), Decimal("0.00"))

    def test_calculate_total_no_discount(self):
        OrderItem.objects.create(order=self.order, unit_price=Decimal("100.00"), quantity=2)
        OrderItem.objects.create(order=self.order, unit_price=Decimal("50.00"), quantity=1)
        total = self.order.calculate_total()
        self.assertEqual(total, Decimal("250.00"))

    @patch("order.utils.calculate_discount")
    def test_calculate_total_with_discounts(self, mock_calc_discount):
        mock_calc_discount.return_value = Decimal("10.00")
        OrderItem.objects.create(order=self.order, unit_price=Decimal("100.00"), quantity=2)
        OrderItem.objects.create(order=self.order, unit_price=Decimal("50.00"), quantity=1)

        total = self.order.calculate_total()
        self.assertEqual(total, Decimal("230.00"))