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
    
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_at_time_of_order = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

# ---------------------------------------Coupon-------------------------------------
 
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"

# -------------------------------------------Discount----------------------------------

class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.percentage}% off)"

# --------------------------------------------Table----------------------------------------

class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()
    is_avaliable = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats)" 