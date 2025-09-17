from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

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