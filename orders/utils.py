from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import string
import secrets
from .models import Order


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

def generate_unique_order_id(length_0):
    characters = string.ascii_uppercase + string.digits 

    while True:
        order_id = "".join(secrets.choice(characters) for _ in range(length))
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id