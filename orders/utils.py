from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import string
import secrets
import logging

from .models import Order   

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

def send_email(recipient, subject, message):
    try:

        validate_email(recipient)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently = False,
        )

        return True

    except ValidationError:
        print(f"Invalid email address: {recipient}")
        return False

    except BadHeaderError:
        print("Invalid header found.")
        return False
    
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def generate_unique_order_id(length=8):

    characters = string.ascii_uppercase + string.digits 

    while True:
        order_id = "".join(secrets.choice(characters) for _ in range(length))
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id

# -----------------------------------------------------------------------------------------



def update_order_status(order_id: int, new_status: str) -> bool:

    try:
        order = Order.objects.get(id=order_id)
        old_status = order.status
        order.status = new_status
        order.save()

        logger.info(f"Order {order_id} status updated from '{old_status}' to '{new_status}'.")
        return True

    except ObjectDoesNotExist:
        logger.error(f"Order with ID {order_id} not found.")
        return False

    except Exception as e:
        logger.exception(f"Error updating status for order {order_id}: {e}")
        return False


# ---------------------------------------------------------------------------------------------

def calculate_order_total(order_items):

    if not order_items:
        return 0.0

    total = 0.0
    for item in order_items:
        quantity = item.get("quantity", 0)
        price = item.get("price", 0.0)
        total += quantity * price

    return total


if __name__ == "__main__":
    order = [
        {"quantity": 3, "price": 20.0},
        {"quantity": 2, "price": 15.5}
    ]

    print(f"Total Order Price: {calculate_order_total(order)}")

# ----------------------------------------------Calculate Discount------------------------------------

def calculate_discount(order_total, discount_percentage):

    try:
        order_total = float(order_total)
        discount_percentage = float(discount_percentage)

        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")

        discount_amount = order_total * (discount_percentage / 100)
        return round(discount_amount, 2)
    
    except (TypeError, ValueError):
        return 0.0

# ---------------------------------------------Calculate_Average_Rating-----------------------------

def calculate_average_rating(review_queryset):

    if not review_queryset.exists():
        return 0.0

    avg_rating = review_queryset.aggregate(Avg('rating'))['rating__avg']
    return float(avg_rating) if avg_rating is not None else 0.0

# -----------------------------------------Get Daily Sales Total------------------------------------

def get_daily_sales_total(target_date: date) -> float:

    total = (
        Order.objects.filter(created_at__date=target_date)
        .aggregate(total_sum=Sum('total_price'))['total_sum']
        or 0
    )
    return float(total)