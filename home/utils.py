import re

# -------------------------------------------calculate_discount---------------------------------------

def calculate_discount(original_price, discount_percentage):

    try:
        original_price = float(original_price)
        discount_percentage = float(discount_percentage)

        if original_price < 0:
            raise ValueError("Original price cannot be negative.")
        if not(0 <= discount_percentage <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")

        discounted_price = original_price * (1 - discount_percentage / 100)
        return round(discounted_price, 2)

    except (ValueError, TypeError) as e:
        print(f"Error calculating discount: {e}")
        return None

# ----------------------------------------Validate Email Address------------------------------------

def validate_email_address(email: str) -> bool:

    email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if re.match(email_regex, email):
        return True
    return False