import string 
import secrets

try:
    from .models import Coupon
    COUPON_MODEL_AVAILABLE = True
    
except ImportError:
    COUPON_MODEL_AVAILABLE = False

def generate_coupon_code(length=10):
    """
    Generate a unique alphanumeric coupon code.
    If Coupon model is avilable, ensure the code is unique in the database.
    """

    alphabet = string.ascii_uppercase + string.digits 

    while True:
        code = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        if COUPON_MODEL_AVAILABLE:
            if not Coupon.objects.filter(code=code).exists():
                return code
        else:
            return code

def main():
    print("Generating 5 sample coupon codes:")
    for _ in range(5):
        print(generate_coupon_code(length=12))
        


if __name__ == "__main__":
    main()