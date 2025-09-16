import logging
from email.utils import parseaddr
import re

logger = logging.getLogger(__name__)

def is_valid_email(email: str) -> bool:

    try:
        if not email:
            return False

        name, addr = parseaddr(email)


        if not addr:
            return False

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, addr):
            return False

        return True 
    
    except Exception as e:
        logger.error(f"Email validation error for '{email}': {e}")
        return False