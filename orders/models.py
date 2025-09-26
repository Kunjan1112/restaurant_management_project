from django.db import models

from django.contrib.auth.models import User

from products.models import Menu

from home.models import MenuItem

from django.conf import settings

# Create your models here.

class ActiveOrderManger(models.Manager):
    def get_active_orders(self):
        return self.filter(status__in=['pending','processing'])

# --------------------------------------Order----------------------------------

class Order(models.Model):
    STATUS_CHOICES =[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def calculate_total_revenue(cls):
        result = cls.objects.filter(status='completed').aggregate(
            total_revenue('total_amount')
        )
        return result['total_revenue'] or 0

# ------------------------------------------OrderItem----------------------------------

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} X {self.quantity}"

# ---------------------------------------Coupon-------------------------------------
 
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_precent = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class OrderQuerySet(models.QuerySet):
    def with_status(self, status):
        return self.filter(status=status)

    def pending(self):
        return self.filter(status="pending")

    def completed(self):
        return self.filter(status="completed")

    def cancelled(self):
        return self.filter(status="cancelled")


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def with_status(self, status):
        return self.get_queryset().with_status(status)

    def pending(self):
        return self.get_queryset().pending()

    def completed(self):
        return self.get_queryset().completed()

    def cancelled(self):
        return self.get_queryset().cancelled()