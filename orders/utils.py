import string 
import secrets

try:
    from .models import Coupon
    COUPON_MODE_AVAILABLE = True

except ImportError:
    COUPON_MODE_AVAILABLE = False

def generate_coupon_code(length=10):
    
    alphabet = string.ascii_uppercase + string.digits 

    while True:
        code = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        if COUPON_MODE_AVAILABLE:
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