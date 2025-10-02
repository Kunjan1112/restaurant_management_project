import re
import datetime

from .models import Table

# -------------------------------------------calculate_discount---------------------------------------

def calculate_discount(price, discount_percentage):

    try:
        original_price = float(original_price)
        discount_percentage = float(discount_percentage)

        if original_price < 0:
            raise ValueError("Original price cannot be negative.")
        if not(0 <= discount_percentage <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")

        discount_amount = (discount_percentage / 100) * original_price
        discount_price = original_price - discount_amount

        return round(discount_price, 2)
    
    except (ValueError, TypeError) as e:
        print(f"Error calculating discount: {e}")
        return None
   
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