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