from django.db import models

from django.contrib.auth.models import User

from products.models import Menu

from home.models import MenuItem

from django.conf import settings

# Create your models here.

class ActiveOrderManger(models.Manager):
    def get_active_orders(self):
        return self.filter(status__in=['pending','processing'])

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    order_status = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def calculate_total(self, save: bool = False) -> Decimal:
        try:
            from orders.utils import calculate_discount
        except Exception:
            def calculate_discount(amount, item=None):
                return Decimal("0.00")

        related_qs = None
        for rel in ("items", "order_items", "orderitem_set"):
            if hasattr(self, rel):
                related_qs = getattr(self, rel).all()
                break

            if related_qs is None:
                total = Decimal("0.00")
                if save:
                    self.total_price = total 
                    self.save(update_fields=["total_price"])
                return total
            
            total = Decimal("0.00")

            for item in related_qs:
                unit_price = getattr(item, "unit_price", None)
                if unit_price is None:
                    unit_price = getattr(item, "price", None)
                if unit_price is None:
                    product = getattr(item, "product", None)
                    unit_price = getattr(product, "price", None) if product is not None else None
                if unit_price is None:
                    unit_price = Decimal("0.00")
                unit_price = Decimal(unit_price)

                quantity = getattr(item, "quantity", 1) or 1
                quantity = Decimal(quantity)

                line_total = unit_price * quantity

                try:
                    discount_result = calculate_discount(line_total, item=item)
                except TypeError:
                    try:
                        discount_result = calculate_discount(line_total)
                    except Exception:
                        discount_result = None
                except Exception:
                    discount_result = None

                if discount_result is None:
                    discounted_line = line_total
                else:
                    try:
                        discount_val = Decimal(discount_result)

                        if discount_val <= line_total:
                            discounted_line = line_total - discount_val
                        else:
                            discounted_line = discount_val
                    except (TypeError, ValueError, InvalidOperation):
                        discounted_line = line_total
                
                total += discounted_line

            total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            if save:
                self.total_price = total
                self.save(update_fields=["total_price"])
            
            return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} X {self.quantity}"
 
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