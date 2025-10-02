import re
import datetime

from .models import Table

# -------------------------------------------calculate_discount---------------------------------------

def calculate_discount(price, discount_percentage):

    if not isinstance(price, (int, float)):
        raise TypeError("Price must be a number (int or float).")
    if not isinstance(discount_percentage, (int, float)):
        raise TypeError("Discount percentage must be a number (int a float).")


    # Validate values
    if price < 0:
        raise ValueError("Price cannot be negative.")
    if not (0 <= discount_percentage <= 100):
        raise ValueError("Discount percentage must be between 0 and 100.")

    # Calculate discounted price
    discount_amount = (price * discount_percentage) / 100
    discounted_price = price - discount_amount

    return round(discounted_price, 2)
   
# ----------------------------------------Validate Email Address------------------------------------

def validate_email_address(email: str) -> bool:

    email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if re.match(email_regex, email):
        return True
    return False

# -------------------------------------------is restaurnat Open--------------------------------------

def is_restaurant_open():
    now = datetime.datetime.now()
    current_day = now.weekday()
    current_day = now.time()

    weekday_open = datetime.time(9, 0)
    weekday_close = datetime.time(22, 0)

    weekend_open = datetime.time(10, 0)
    weekend_close = datetime.time(23, 0)

    if current_day < 5:
        return weekday_open <= current_time <= weekday_close

    else:
        return weekend_open < current_time <= weekend_close

# ----------------------------------------------get_available_tables_by_capacity----------------------------------

def get_available_tables_by_capacity(num:guests: int):
    return Table.objects.filter(
        is_available=True,
        capacity__gte = num_guests
    ).order_by('capacity')