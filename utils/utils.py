import re

def format_phone_number(phone: str) -> str:
    try:
        if not phone:
            return ""

        digits = re.sub(r"\D", "", phone)

        if len(digits) == 10:
            return f"({digits[0:3]}) {digits[3:6]}-{digits[6:10]}"
        elif len(digits) == 11 and digits.startswith("1"):
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:11]}"
        else:
            return phone
    except Exception:
        return phone