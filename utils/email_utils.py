from django.core.mail import send_mail, BadHeaderError

from django.conf import settings

import logging

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order_id, customer_email, customer_name, total_amount):
    
    subject = f"Order Confirmation - Order #{order_id}"
    message = (
        f"Hello {customer_name}, \n\n"
        f"Thank you for your order!\n\n"
        f"Your order ID is: {order_id}\n"
        f"Total Amount: {total_amount}\n\n"
        f"We will notify you once your order is shipped.\n\n"
        f"Regards, \nThe Restaurant Team"
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, from_email, [customer_email])
        return {"status": "success", "message":"Email sent successfully"}
    except BadHeaderError:
        logger.error("Invalid header found while sending order confirmation email.")
        return {"status":"error", "message":"Invalid header found."}
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return {"status": "error", "meassage":f"Failed to send email. Reason: {str(e)}"}